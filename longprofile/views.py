from django.shortcuts import render, get_object_or_404
from longprofile.forms import *
from longprofile.models import *
from byhand.models import *
import json
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.urls import reverse
from longprofile.urls import url
from django.urls import resolve
import datetime as dt
from datetime import datetime
import datetime
from social.models import *

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
import base64
# from django.shortcuts import (
# render_to_response
# )
from django.template import RequestContext
from django.contrib.auth.decorators import login_required




# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,'longprofile/home.html')
@login_required(login_url='login')
def cards(request):
    return render(request,'longprofile/cards.html')
@login_required(login_url='login')
def company_card_update(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    current_user = request.user
    if Company_card.objects.filter(user_id = current_user.id):
        view = Company_card.objects.get(user_id = current_user.id)
        if request.method == "POST":
            try:
                view.front_img = request.FILES['uploadFront']
            except:
                view.front_img = view.front_img
            try:
                view.back_img = request.FILES['uploadBack']
            except:
                view.back_img = view.back_img
            view.name = request.POST['name']
            view.company_name = request.POST['companyname']
            view.services = request.POST['services']
            view.mobile = request.POST['mobile']
            view.whatsapp = request.POST['whatsapp']
            view.company_name = request.POST['companyname']
            view.website = request.POST['website']
            view.email = request.POST['email']
            view.location = request.POST['location']
            view.company_location = request.POST['companylocation']
            view.aditional_details = request.POST['addtionaldetails']
            view.user_id = current_user.id
            view.save()
    else:  
        view = Company_card()
        if request.method == "POST":
            view.front_img = request.FILES['uploadFront']
            view.back_img = request.FILES['uploadBack']
            view.name = request.POST['name']
            view.company_name = request.POST['companyname']
            view.services = request.POST['services']
            view.mobile = request.POST['mobile']
            view.whatsapp = request.POST['whatsapp']
            view.company_name = request.POST['companyname']
            view.website = request.POST['website']
            view.email = request.POST['email']
            view.location = request.POST['location']
            view.company_location = request.POST['companylocation']
            view.aditional_details = request.POST['addtionaldetails']
            view.user_id = current_user.id
            view.save()
    context = {
        'company':company,
    }
    return render(request,'longprofile/company_card_update.html',context)
@login_required(login_url='login')
def personal_card_update(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    current_user = request.user  
    view = Personal_card()
    if request.method == "POST":
        view.front_img = request.FILES['uploadFront']
        view.back_img = request.FILES['uploadBack']
        view.name = request.POST['name']
        view.company_name = request.POST['companyname']
        view.services = request.POST['services']
        view.mobile = request.POST['mobile']
        view.whatsapp = request.POST['whatsapp']
        view.company_name = request.POST['companyname']
        view.website = request.POST['website']
        view.email = request.POST['email']
        view.location = request.POST['location']
        view.company_location = request.POST['companylocation']
        view.aditional_details = request.POST['addtionaldetails']
        view.user_id = current_user.id
        view.save()
    context = {
        'company':company,
    }
    return render(request,'longprofile/personal_card_update.html',context)
@login_required(login_url='login')
def personalcardDelete(request,pk):
    try:
        personalcard = Personal_card.objects.get(pk=pk)
        personalcard.delete()
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def personalcardview(request,pk,slug):
    personalcard = Personal_card.objects.get(pk=pk)
    allpersonalcard = Personal_card.objects.filter(user_id=slug)
    context = {
        'personalcard':personalcard,
        'allpersonalcard':allpersonalcard,
        'otheruser_id':slug,
        'pk':pk
    }
    return render(request,'longprofile/personalcardview.html',context)
@login_required(login_url='login')
def personalcardviewpdf(request,pk):
    personalcard = Personal_card.objects.get(pk=pk)
    context = {
        'personalcard':personalcard,
        'pk':pk,
    }
    pdf = render_to_pdf('longprofile/personalcardviewpdf.html',context)
    return HttpResponse(pdf,content_type='application/pdf')
@login_required(login_url='login')
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
@login_required(login_url='login')
def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = CustomUser.objects.filter(first_name__icontains = query_original)
    mylist = []
    mylist += [x.first_name for x in queryset]
    return JsonResponse(mylist,safe = False)
@login_required(login_url='login')
def manualsearch(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    try:
        bio_currentuser = Bio.objects.get(user_id = request.user.id)
    except:
        bio_currentuser = ''
    if request.method == 'GET':
        search = request.GET.get('tags')
        searching = CustomUser.objects.filter(Q(first_name__icontains = search) | Q(username__icontains=search) | Q(email__icontains=search)).exclude(id=request.user.id)
        endorsed = [ i for i in searching if Endorse.objects.filter(user_id = request.user.id, liked_person_id = i.id)]
        followed = [ j for j in searching if Follow2.objects.filter(following_id = request.user.id, follower_id = j.id)]
        connectionaccept = [ k for k in searching if Connection.objects.filter(Q(connected_person_id=request.user.id, user_id=k.id, connection=1) | Q(user_id=request.user.id, connected_person_id=k.id, connection=1))]
        connectionrequest = [l for l in searching if Connection.objects.filter(user_id = request.user.id, connected_person_id = l.id, connection = 0)]
        a = (len(searching))
        if a<= 0:
            # return HttpResponse("We couldn't find a match for " + search)
            return render(request,'longprofile/emptysearch.html',{"search":search})
    context = {
        'searching':searching,
        'bio_currentuser':bio_currentuser,
        'company':company,
        'endorsed':endorsed,
        'followed':followed,
        'connectionaccept':connectionaccept,
        'connectionrequest':connectionrequest
    }
    return render(request,'longprofile/search.html',context)
@login_required(login_url='login')
def searchprofile_full_view(request, pk):
    company = request.user.groups.filter(name='COMPANY').exists()
    request.session['othreuser'] = pk
    instance = get_object_or_404(CustomUser, pk=pk)
    try:
        bio_currentuser = Bio.objects.get(user_id = request.user.id)
    except:
        bio_currentuser = ''
    try:
        biodata = Bio.objects.get(user_id = pk)
    except:
        biodata = ''
    try:
        achivements = Achievements.objects.get(user_id = pk)
    except:
        achivements = ''
    userextend = UserExtend.objects.get(user_id = pk)
    is_following = Follow2.objects.filter(following_id = request.user.id, follower_id = pk)
    endorse = Endorse.objects.filter(user_id = request.user.id, liked_person_id = pk)
    if Connection.objects.filter(user_id = request.user.id, connected_person_id = pk, connection = 0):
        is_connection = "requested"
    elif Connection.objects.filter(Q(connected_person_id=request.user.id, user_id=pk, connection=1) | Q(user_id=request.user.id, connected_person_id=pk, connection=1)):
        is_connection = "connected"
    else:
        is_connection = "notConnected"
    following_count = Follow2.objects.filter(following_id = pk).count()
    follower_count = Follow2.objects.filter(follower_id = pk).count()
    endorse_count = Endorse.objects.filter(liked_person_id = pk).count()
    connection_count = Connection.objects.filter(Q(connected_person_id=request.user.id, connection=1) | Q(user_id=request.user.id, connection=1)).count()
    otheruser_id = int(pk)
    #star rating view
    try:
        rating_view = Rating.objects.filter(rated_person = pk).aggregate(Sum('rating'))
        rating_count = Rating.objects.filter(rated_person = pk).count()
        e = (rating_view['rating__sum'])
        rating = e/rating_count
    except:
        rating = 0
    expertise = Expertise.objects.filter(user_id=pk)
    experience = Experience.objects.filter(user_id=pk)
    projects = Projects.objects.filter(user_id=pk)
    achievements = Achievements.objects.filter(user_id=pk)
    certification = Certificate.objects.filter(user_id=pk)
    clientinfo = Client.objects.filter(user_id=pk)
    testimonial = Testimonial.objects.filter(user_id=pk)
    try:
        about = Aboutdetails.objects.get(user_id=pk)
    except:
        about = ""
    try:
        personalcard = Personal_card.objects.filter(user_id=pk).last()
    except:
        personalcard = ""
    try:
        companycard = Company_card.objects.get(user_id=pk)
    except:
        companycard = ""
    try:
        if Connection.objects.get(Q(connected_person_id=request.user.id, user_id=pk, connection=1) | Q(user_id=request.user.id, connected_person_id=pk, connection=1)):
            chaticonhide = True
        else:
            chaticonhide = False
    except:
        chaticonhide = False
    context = {
        'instance':instance,
        'bio_currentuser':bio_currentuser,
        'biodata':biodata,
        'userextend':userextend,
        'connection':is_following,
        'endorse':endorse,
        'following_count':following_count,
        'rating':rating,
        'follower_count':follower_count,
        'is_connection':is_connection,
        'endorse_count':endorse_count,
        'connection_count':connection_count,
        'otheruser_id':otheruser_id,
        'expertise':expertise,
        'experience':experience,
        'projects':projects,
        'achievements':achievements,
        'certification':certification,
        'clientinfo':clientinfo,
        'testimonial':testimonial,
        'personalcard':personalcard,
        'companycard':companycard,
        'chaticonhide':chaticonhide,
        'company':company,
        'about':about,
    }
    return render(request,'longprofile/searchpofile_full_view.html',context)
@login_required(login_url='login')
def profile_full_view(request):
    return render(request,'longprofile/profile_full_view.html')
@login_required(login_url='login')
def countAndNotifications(request,pk):
    pk = request.session['othreuser']
    follower_count = Follow2.objects.filter(follower_id = pk).count()
    if Connection.objects.filter(user_id = request.user.id, connected_person_id = pk, connection = 0):
        is_connection = "Requested"
    elif Connection.objects.filter(Q(connected_person_id=request.user.id, user_id=pk, connection=1) | Q(user_id=request.user.id, connected_person_id=pk, connection=1)):
        is_connection = "Connected"
    else:
        is_connection = "Connect+"
    pendingRequest = Connection.objects.filter(connected_person_id = request.user.id, connection = 0)
    html = ""
    for i in pendingRequest:
        html="""
        <div>
            <p style="display: inline-block;">%s</p>
            <a type="button" class="btn btn-success" id="connections_accept" role="button" href="/longprofile/connectionAccept/%s">Accept</a>
            <a type="button" class="btn btn-danger" id="connections_remove" role="button" href="/longprofile/connectionDelete/%s">Remove</a>
        </div>
        """
        # current_url = resolve(request.path_info)
        html = html % (i.user.first_name,i.pk,i.pk)
    resp = {
        "follower_count":follower_count,
        'is_connection':is_connection,
        "data":html
        
    }
    data = json.dumps(resp)
    return HttpResponse(data,content_type = "application/json")
@login_required(login_url='login')
def home2(request):
    
    return render(request,'longprofile/home2.html')
@login_required(login_url='login')
def starRating(request):
    current_user = request.user
    othreuser = request.session['othreuser']
    if Rating.objects.filter(user_id = current_user.id, rated_person = othreuser):
        view = Rating.objects.get(user_id = current_user.id, rated_person = othreuser)
        if request.method == "POST":
            view.user_id = current_user.id
            view.rated_person = othreuser
            r = request.POST['rating']
            view.rating = float(r)
            view.save()
    else:
        if request.method == "POST":
            data = Rating()
            data.user_id = current_user.id
            data.rated_person = othreuser
            r = request.POST['rating']
            data.rating = float(r)
            data.save()
    return HttpResponse("rating is not working.we are working to fix it")
@login_required(login_url='login')
def follow(request, pk):
    main_user = request.user.id
    othreuser = pk
    #check if already following
    if Follow2.objects.filter(following_id = main_user, follower_id = othreuser):
        unfollow = Follow2.objects.get(following_id = main_user, follower_id = othreuser)
        unfollow.delete()
        notify = Notification.objects.filter(sender_id = main_user,notification_type = 4,user_id = othreuser)
        notify.delete()
        is_following = False
        following_count = Follow2.objects.filter(following_id = pk).count()
    else:
        foll2 = Follow2()
        foll2.follower_id=othreuser
        foll2.following_id = main_user
        foll2.save()
        notify = Notification()
        # notify.post_id = foll2.id
        notify.sender_id = main_user
        notify.user_id = othreuser
        notify.notification_type=4
        notify.save()
        is_following = True
        following_count = Follow2.objects.filter(following_id = pk).count()
    resp = {
        "following":is_following,
        "following_count":following_count,
        "othreuser":othreuser
    }
    response = json.dumps(resp)
    return HttpResponse(response,content_type="application/json")
@login_required(login_url='login')
def endorse(request,pk):
    main_user = request.user.id
    othreuser = pk
    if Endorse.objects.filter(user_id = main_user, liked_person_id = othreuser):
        unendorse = Endorse.objects.get(user_id = main_user, liked_person_id = othreuser)
        unendorse.delete()
        notify = Notification.objects.filter(sender_id = main_user,notification_type = 5,user_id = othreuser)
        notify.delete()
        is_endorsing = False
    else:
        endorse = Endorse()
        endorse.user_id = main_user
        endorse.liked_person_id = othreuser
        endorse.save()
        notify = Notification()
        notify.sender_id = main_user
        notify.user_id = othreuser
        notify.notification_type=5
        notify.save()
        is_endorsing = True
    resp = {
        "endorsing":is_endorsing,
        "othreuser":othreuser
    }
    response = json.dumps(resp)
    return HttpResponse(response,content_type="application/json")
@login_required(login_url='login')
def connection(request,pk):
    main_user = request.user.id
    othreuser = pk
    if Connection.objects.filter(user_id = main_user, connected_person_id = othreuser):
        disconnect = Connection.objects.get(user_id = main_user, connected_person_id = othreuser)
        disconnect.delete()
        notify = Notification.objects.filter(sender_id = main_user,notification_type = 6,user_id = othreuser)
        notify.delete()
        is_connection = "notConnected"
    elif Connection.objects.filter(user_id = main_user, connected_person_id = othreuser, connection = 0):
        is_connection = "requested"
    elif Connection.objects.filter(Q(connected_person_id=request.user.id, user_id=pk, connection=1) | Q(user_id=request.user.id, connected_person_id=pk, connection=1)):
        is_connection = "connected"
    else:
        conn = Connection()
        conn.user_id = main_user
        conn.connected_person_id = othreuser
        conn.save()
        notify = Notification()
        notify.sender_id = main_user
        notify.user_id = othreuser
        notify.notification_type=6
        notify.save()
        is_connection = "requested"
    resp = {
        "isconnection":is_connection,
        "othreuser":othreuser
    }
    response = json.dumps(resp)
    return HttpResponse(response,content_type="application/json")
@login_required(login_url='login')
def connectionList(request,pk):
    company = request.user.groups.filter(name='COMPANY').exists()
    instance = get_object_or_404(CustomUser, pk=pk)
    pendingRequest = Connection.objects.filter(connected_person_id = request.user.id, connection = 0)
    myConnections = Connection.objects.filter(Q(user_id = pk, connection = 1) | Q(connected_person_id = pk, connection = 1))
    context = {
        'instance':instance,
        'pendingRequest':pendingRequest,
        'myConnections':myConnections,
        'company':company
    }
    return render(request,"longprofile/connectionlist.html",context)
@login_required(login_url='login')
def connectionDelete(request,pk):
    # othreuser = request.session['othreuser']
    d = Connection.objects.get(pk=pk)
    d.delete()
    return HttpResponseRedirect(reverse("connectionList",kwargs={'pk':request.user.id}))
@login_required(login_url='login')
def connectionAccept(request,pk):
    # othreuser = request.session['othreuser']
    view=Connection.objects.get(pk=pk)
    view.connection = 1
    view.save()
    return HttpResponseRedirect(reverse("connectionList",kwargs={'pk':request.user.id}))
#event
@login_required(login_url='login')
def createevent(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    current_user = request.user
    form = CreateEventForm()
    if request.method == "POST":
        form = CreateEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user_id = current_user.id
            event.save()
            return HttpResponseRedirect(reverse("event"))
    my_event = CreateEvent.objects.filter(user_id = current_user.id)
    savedEventView = SavedEvent.objects.filter(savedperson_id = current_user.id)
    context = {
        "form":form,
        "my_event":my_event,
        "savedEventView":savedEventView,
        'company':company
    }
    return render(request,'longprofile/event.html',context)
@login_required(login_url='login')
def eventOtheruser(request,pk):
    company = request.user.groups.filter(name='COMPANY').exists()
    current_user = request.user
    my_event = CreateEvent.objects.filter(user_id = pk)
    saved_event = [i for i in my_event if SavedEvent.objects.filter(savedperson_id = current_user.id,event_id = i)]
    context = {
        "my_event":my_event,
        "saved_event":saved_event,
        'company':company
    }
    return render(request,'longprofile/eventOtheruser.html',context)
@login_required(login_url='login')
def eventSave(request,pk):
    company = request.user.groups.filter(name='COMPANY').exists()
    main_user = request.user
    events = int(pk)
    if SavedEvent.objects.filter(event_id = events,savedperson_id = main_user.id):
        unsave = SavedEvent.objects.get(event_id = events,savedperson_id = main_user.id)
        unsave.delete()
        is_save = False
    else:
        saving = SavedEvent()
        saving.event_id = pk
        saving.savedperson_id = main_user.id
        saving.save()
        is_save = True
    resp = {
        "is_save":is_save,
        "save_id":pk
    }
    response = json.dumps(resp)
    return HttpResponse(response,content_type="application/json")
@login_required(login_url='login')
def deleteevent(request,pk):
    savedevent = SavedEvent.objects.get(id=pk)
    savedevent.delete()
    return HttpResponseRedirect(reverse("event"))
#enquiry
@login_required(login_url='login')
def createEnquiry(request,pk):
    company = request.user.groups.filter(name='COMPANY').exists()
    current_user = request.user
    other_user = int(pk)
    form = CreateEnquiryForm()
    if current_user.id != other_user:
        if request.method == "POST":
            form = CreateEnquiryForm(request.POST)
            if form.is_valid():
                enquiry = form.save(commit=False)
                enquiry.user_id = current_user.id
                enquiry.enquired_person_id = other_user
                enquiry.save()
                return HttpResponseRedirect(reverse("createEnquiry",kwargs={'pk':other_user}))
    context = {
        "form":form,
        'company':company
    }
    return render(request,'longprofile/enquiry.html',context)
@login_required(login_url='login')
def myenquiry(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    current_user = request.user
    enquiries = CreateEnquiry.objects.filter(enquired_person_id = current_user.id)
    myenquies = CreateEnquiry.objects.filter(user_id = current_user.id)
    savedenquiries = [i for i in enquiries if SavedEnquiry.objects.filter(savedperson_id = current_user.id,enquiry_id = i)]
    savedEnquiryView = SavedEnquiry.objects.filter(savedperson_id = current_user.id)
    context = {
        "enquiries":enquiries,
        "myenquies":myenquies,
        "savedenquiries":savedenquiries,
        "savedEnquiryView":savedEnquiryView,
        'company':company
    }
    return render(request,'longprofile/myenquiry.html',context)
@login_required(login_url='login')
def enquirySave(request,pk):
    main_user = request.user
    enquiry = int(pk)
    if SavedEnquiry.objects.filter(enquiry_id = enquiry,savedperson_id = main_user.id):
        unsave = SavedEnquiry.objects.get(enquiry_id = enquiry,savedperson_id = main_user.id)
        unsave.delete()
        is_save = False
    else:
        saving = SavedEnquiry()
        saving.enquiry_id = pk
        saving.savedperson_id = main_user.id
        saving.save()
        is_save = True
    resp = {
        "is_save":is_save,
        "save_id":pk
    }
    response = json.dumps(resp)
    return HttpResponse(response,content_type="application/json")
@login_required(login_url='login')
def deleteenquiry(request,pk):
    savedenquiry = SavedEnquiry.objects.get(id=pk)
    savedenquiry.delete()
    return HttpResponseRedirect(reverse("enquiry"))
#appoinment
@login_required(login_url='login')
def createAppoinment(request,pk):
    company = request.user.groups.filter(name='COMPANY').exists()
    current_user = request.user
    username = current_user.first_name
    other_user = int(pk)
    form = CreateAppoinmentForm()
    if current_user.id != other_user:
        if request.method == "POST":
            appoinment = CreateAppoinment2()
            appoinment.name = request.POST['name']
            appoinment.purpose = request.POST['purpose']
            appoinment.description = request.POST['description']
            a =request.POST['date']
            b = request.POST['time']
            bb = b.replace(":","")
            new_date = datetime.datetime.strptime(a, '%Y-%m-%d')
            mytime = dt.datetime.strptime(bb,'%H%M').time()
            c = dt.datetime.combine(new_date, mytime)
            appoinment.dateandtime = c
            appoinment.user_id = current_user.id
            appoinment.enquired_person_id = other_user
            appoinment.save()
            return HttpResponseRedirect(reverse("createAppoinment",kwargs={'pk':other_user}))
    context = {
        "form":form,
        "username":username,
        'company':company
    }
    return render(request,'longprofile/appoinment.html',context)
@login_required(login_url='login')
def myappoinment(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    date = datetime.datetime.now()
    current_user = request.user
    # current_time = date.strftime("%X")
    # current_date = date.strftime("%Y-%m-%d")
    pending = CreateAppoinment2.objects.filter(dateandtime__gte = date,active = 0,enquired_person_id = current_user.id)
    actived = CreateAppoinment2.objects.filter(dateandtime__gte = date,active = 1,enquired_person_id = current_user.id)
    complete = CreateAppoinment2.objects.filter(dateandtime__lte = date,enquired_person_id = current_user.id)
    requested = CreateAppoinment2.objects.filter(user_id = current_user.id)
    context = {
        "pending":pending,
        "actived":actived,
        "complete":complete,
        "requested":requested,
        'company':company
    }
    return render(request,'longprofile/myappoinment.html',context)
@login_required(login_url='login')
def approveappointment(request,pk):
    view = CreateAppoinment2.objects.get(id=pk)
    view.active = 1
    view.save()
    return HttpResponseRedirect(reverse("appointment"))
@login_required(login_url='login')
def updateappointment(request,id):
    view = CreateAppoinment2.objects.get(id=id)
    # view2 = view.dateandtime
    # dateview = view2.strftime("%Y-%m-%d")
    # timeview = view2.strftime("%H:%M")
    if request.method =='POST':
        a =request.POST.get('date')
        b = request.POST.get('time')
        bb = b.replace(":","")
        new_date = datetime.datetime.strptime(a,'%Y-%m-%d')
        mytime = dt.datetime.strptime(bb,'%H%M').time()
        c = dt.datetime.combine(new_date, mytime)
        view.dateandtime = c
        view.save()

    # context = {
    #     "dateview":dateview,
    #     "timeview":timeview
    # }
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def deleteappointment(request,pk):
    view = CreateAppoinment2.objects.get(id=pk)
    view.delete()
    return HttpResponseRedirect(reverse("appointment"))
#longprofile delete
@login_required(login_url='login')
def expertisedelete(request,pk):
    expertise = Expertise.objects.get(pk=pk)
    expertise.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def experiencedelete(request,pk):
    experience = Experience.objects.get(pk=pk)
    experience.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def projectsdelete(request,pk):
    projects = Projects.objects.get(pk=pk)
    projects.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def achievementsdelete(request,pk):
    achievements = Achievements.objects.get(pk=pk)
    achievements.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def certificationdelete(request,pk):
    certificate = Certificate.objects.get(pk=pk)
    certificate.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def clientdelete(request,pk):
    client = Client.objects.get(pk=pk)
    client.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def testimonialdelete(request,pk):
    testimonial = Testimonial.objects.get(pk=pk)
    testimonial.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#404 reeoe page
def not_found(request, exception=None):
    response = render(request, 'longprofile/404.html', {})
    response.status_code = 404
    return response
def server_error(request, exception=None):
    response = render(request, 'longprofile/404.html', {})
    response.status_code = 500
    return response
@login_required(login_url='login')
def aboutupdate(request):
    if Aboutdetails.objects.filter(user_id = request.user.id):
        about = Aboutdetails.objects.get(user_id = request.user.id)
        about.user_id = request.user.id
        about.description = request.POST.get('about')
        
        about.save()
    else:
        about = Aboutdetails()
        about.user_id = request.user.id
        about.description = request.POST.get('about')
        about.save()
    return HttpResponse('')
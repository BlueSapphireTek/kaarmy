import json
# import simplejson
import phonenumbers
from datetime import datetime
from phonenumbers import geocoder
from phonenumbers import carrier
import string,random
from django.db.models import Q

from django.http import HttpResponse,HttpResponseRedirect

from django.shortcuts import render, redirect

# Create your views here.
from social.models import Post,Report

from social.forms import PostForm

from byhand.models import Follow,UserExtend,CustomUser,Bio
from longprofile.models import Follow2,Endorse,Connection

from social.models import Like,Comment,Achievement,Projects,Cexepertise,About,Expertise,Achievements,Experience,Certificate,Enquiry,Testimonial,Client,Branch ,Working ,Notification,Brousher,Cards,Image,Documents,Location


from social.forms import WorkingForm,AboutForm,ClientForm
from googletrans import  Translator
from django.forms import  modelformset_factory
from django.contrib.auth.decorators import login_required




from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from social.forms import ExpertiseForm,AchievementsForm,ProjectsForm,ExperienceForm,TestimonialForm,CertificateForm,BranchForm
from newsapi import NewsApiClient
from longprofile.models import *

@login_required(login_url = 'login')
def PostView(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            a = form.cleaned_data['caption']
            b = form.cleaned_data['file']
            p =request.POST.get('privacy')
            post.user_id = request.user.id
            c= request.user.id 
            post.privacy = p
            
            post.save()







        # Cmnt = request.POST.get('caption')
        # img = request.POST.get('image')
        # post = Post()
        # post.caption = Cmnt
        # post.image = img
        # post.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def index(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    

    fol = Follow.objects.filter(follower_id = request.user.id)

    group_ids = []
    for i in fol:
        group_ids.append(i.following_id)


    
    post_items = Post.objects.filter(user_id__in=group_ids).all()
    



    liked = Like.objects.filter(user_id=request.user.id).exists()

    if request.method == "POST":
        id = request.POST.get('id')
        comment = request.POST.get('comment')
        commentv = Comment()
        commentv.comment = comment
        commentv.post_id = id
        commentv.user_id = request.user.id
        comment.bio_id == request.user.id
        commentv.save()
        post = Post.objects.get(id = id)
        
        current_comments = post.comments
        post.comments = current_comments + 1
        post.save()








    # pos = Post.objects.filter(user_id = request.user.id)
    context = {
        'liked':liked,
        'post_items': post_items,
        'company':company,


    }

    return render(request,'index.html',context)


@login_required(login_url = 'login')
def timeline(request):
    
    try:
        userextend = UserExtend.objects.get(user_id = request.user.id)
    except:
        return redirect('register_as')
    newsapi = NewsApiClient(api_key='c0418e40b3a04a9b8e853126e29d8f7a')
    top_headlines = newsapi.get_top_headlines(q='covid',language='en',country='in')
    ntitle = top_headlines['articles'][0]['title']
    ndes = top_headlines['articles'][0]['description']
    nurl = top_headlines['articles'][0]['url']
    nimg = top_headlines['articles'][0]['urlToImage']

    

    
    
    company = request.user.groups.filter(name='COMPANY').exists()
    try:
        bioview = Bio.objects.get(user_id = request.user.id)
    except:
        bioview = ""
        
        

    fol = Follow2.objects.filter(following_id=request.user.id)
    
    _x = Post.objects.all()
   


    group_ids = []
    group_ids.append(request.user.id)
    # group_ids.append(1)
    
    if fol:
        for i in fol:
            group_ids.append(i.follower_id)
        

    
    post_items = Post.objects.filter(user_id__in=group_ids,privacy = 1,is_deleted = 0).all()

    liked_posts = [i for i in post_items if Like.objects.filter(post_id = i,user_id = request.user.id )]


    comments = [i for i in post_items if Comment.objects.filter(post_id = i)]

    
   


    context = {
        'userextend':userextend,
        'post_items':post_items,
        'liked_posts':liked_posts,
        'comments':comments,
        'bioview':bioview,
        'company':company,
        'ntitle':ntitle,
        'ndes':ndes,
        'nurl':nurl,
        'nimg':nimg
    }
    return render(request,'timeline/timeline.html',context)




@login_required(login_url = 'login')
def like(request,id):


    # if liked:
    #     dislike = Like.objects.filter(post_id = id)
    #     dislike.delete()
    #     liked = False
    #     return HttpResponse('true')
    # else:


    like=Like()
    like.user_id = request.user.id
    like.post_id = id
    like.save()

    post = Post.objects.get(id=id)
    current_like = post.likes
    post.likes = current_like +1
    post.save()
    return redirect('index')

@login_required(login_url = 'login')
def dislike(request,id):
     dislike = Like.objects.filter(post_id = id)
     dislike.delete()

     post = Post.objects.get(id=id)
     current_like = post.likes
     post.likes = current_like - 1
     post.save()
     return redirect('index')


@login_required(login_url = 'login')
def postlike(request,id):
    
    liked = Like.objects.filter(user_id = request.user.id,post_id = id)
    lc = Like.objects.filter(post_id = id).count()
    

    post = Post.objects.get(id = id)
    p = post.user.id
    
    is_liked = True if liked else False
    if is_liked:
        liked.delete()
        notify = Notification.objects.filter(post = post ,sender = request.user.id,notification_type = 1)
        notify.delete()
        is_liked = False
        lcn = Like.objects.filter(post_id = id).count()

    else:
        like = Like()
        like.user_id = request.user.id
        like.post_id = id
        like.save()
        notify = Notification()
        notify.post_id = id
        
        if request.user.id != post.user.id:
            notify.sender_id = request.user.id
            notify.user_id = p
            notify.notification_type= 1
            notify.save()
        is_liked = True
        lcn = Like.objects.filter(post_id = id).count()

    resp = {
        "liked":is_liked,
        "post_id":id,
        "lcn":lcn,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


@login_required(login_url = 'login')

def likecount(request,id):
    likescount = Like.objects.filter(post_id = id).count()

    return render(request,'index.html',{'likescount':likescount})

# def comment(request):
#
#         return HttpResponse('sucess')
#
#     return render(request,'index.html')


@login_required(login_url = 'login')
def post_detail(request,id):
    company = request.user.groups.filter(name='COMPANY').exists()
    digits = ''.join(random.sample(string.digits, 2))
    chars = ''.join(random.sample(string.ascii_lowercase, 3))
    

    liked_posts = Like.objects.filter(user_id = request.user.id,post_id = id)
    post = Post.objects.get(id=id)
    comment = Comment.objects.filter(post_id = id)

    context = {
        'post':post,
        'comment':comment,
        'liked_posts':liked_posts,
        'company':company
    }
    return render(request,'timeline/post_details_page.html',context)




@login_required(login_url = 'login')
def comment(request):
    if request.method == "POST":
        post = request.POST.get('commentid')
        commentfeed = request.POST.get('comments')

        postid = int(post)
        p = Post.objects.get(id = postid)
        
        sender = p.user.id
       
        comment = Comment()
        comment.post_id = post
        comment.user_id = request.user.id
        
        comment.comment = commentfeed
        comment.save()

        # bio = Bio.objects.get(id = request.user.id)
        # profile = bio.image

        notify = Notification()
        notify.post_id = post
        notify.user_id = sender
        if request.user.id != p.user.id:
        
            notify.sender_id =request.user.id
            notify.notification_type = 2
            notify.save()

        comment_list = []

        comment_list = [{
            "sender" : request.user.id,
            "comment": commentfeed,
        }]

        return JsonResponse(comment_list, safe=False)



        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
    
@login_required(login_url = 'login')
@csrf_exempt
def postreport(request):
    if request.method == "POST":
        postid = request.POST.get('postid')
        report = request.POST.get('gender')
       
        
        postreport = Report()
        postreport.post_id = postid
        postreport.content = report
        postreport.reporter_id =request.user.id
        postreport.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


def postDelete(request):
    a = request.POST.get('id')
    d = Post.objects.get(pk=a)
    d.is_deleted = 1
    d.save()
    return HttpResponse('')

@login_required(login_url = 'login')
def enquiry(request):
    if request.method == "POST":
        enquirytitle = request.POST.get('enquiry-name')
        enquirydescription = request.POST.get('enquiry-description')

        enquiry = Enquiry()
        enquiry.user_id = request.user.id
        enquiry.title = enquirytitle
        enquiry.description = enquirydescription
        enquiry.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = 'login')
def profile(request):
    

    return render(request,'profile/profile.html')


@login_required(login_url = 'login')
def companyprofile(request):
    print(request.user.id)
    
    try:
        userextend = UserExtend.objects.get(user_id = request.user.id)
    except:
        return redirect('register_as')
    
    company = request.user.groups.filter(name='COMPANY').exists()
    

    try:
        bioview = Bio.objects.get(user_id = request.user.id)
    except:
        bioview =""
        
    try:
        location = Location.objects.get(user_id = request.user.id)
    except:
        location = ''
        
    try:
        abouth = Aboutdetails.objects.get(user_id=request.user.id)
    except:
        abouth = ""

    
    form = WorkingForm()
    expertiselist = Expertise.objects.filter(user_id=request.user.id)
    achievements = Achievements.objects.filter(user_id=request.user.id)
    projects = Projects.objects.filter(user_id=request.user.id)
    certificates = Certificate.objects.filter(user_id=request.user.id)
    clients = Client.objects.filter(user_id = request.user.id)
    branches = Branch.objects.filter(user_id = request.user.id)

    testimonial = Testimonial.objects.filter(user_id= request.user.id)
    companies = CustomUser.objects.all()
    AchievementFormSet = modelformset_factory(Achievement, fields=('name',), extra=3)
    formset = AchievementFormSet(queryset=Achievement.objects.filter(user_id=request.user.id))
    
    following_count = Follow2.objects.filter(following_id = request.user.id).count()
    follower_count = Follow2.objects.filter(follower_id = request.user.id).count()
    endorse_count = Endorse.objects.filter(liked_person_id =request.user.id).count()
    connection_count = Connection.objects.filter(Q(connected_person_id=request.user.id, connection=1) | Q(user_id=request.user.id, connection=1)).count()
    try:
        about = About.objects.get(user_id = request.user.id).about
        a = 1
        
    except:
        about = "None"
        a = 2
        


    try:
        monview = Working.objects.get(day =1 , user_id = request.user.id)
        
    except:
        monview = ''
        

    try:
        tueview = Working.objects.get(day =2,user_id = request.user.id )
        
    except:
        tueview = ''
        

    try:
        wedview = Working.objects.get(day =3,user_id = request.user.id )
        
    except:
        wedview = ''
        

    try:
        thuview = Working.objects.get(day =4,user_id = request.user.id )
        
    except:
        thuview = ''
        

    try:
        friview = Working.objects.get(day =5,user_id = request.user.id )
        
    except:
        friview = ''
        

    try:
        satview = Working.objects.get(day =6,user_id = request.user.id )
        
    except:
        satview = ''
        

    try:
        sunview = Working.objects.get(day =7,user_id = request.user.id )
        
    except:
        sunview = ''
        


    context = {
        'form':form,
        'formset':formset,
        'userextend':userextend,
        'about':about,
        'expertiselist':expertiselist,
        'achievements':achievements,
        'projects':projects,
        'certificates':certificates,
        'companies':companies,
        'clients':clients,
        'branches':branches,
        'testimonial':testimonial,
        'monview':monview,
        'tueview':tueview,
        'wedview':wedview,
        'thuview':thuview,
        'friview':friview,
        'satview':satview,
        'sunview':sunview,
        'bioview':bioview,
        'company':company,
        'location':location,
        
        'following_count':following_count,
        'follower_count':follower_count,
        'endorse_count':endorse_count,
        'connection_count':connection_count,
        'abouth':abouth,

    }
    return render(request,'profile/profile-company-edit.html',context)

@login_required(login_url = 'login')
def userprofile(request):
    
    try:
        userextend = UserExtend.objects.get(user_id = request.user.id)
    except:
        return redirect('register_as')
    company = request.user.groups.filter(name='COMPANY').exists()

    
    all_users = CustomUser.objects.values_list('first_name', flat=True)
    
    all_img = Bio.objects.all().distinct()
    try:
        abouth = Aboutdetails.objects.get(user_id=request.user.id)
    except:
        abouth = ""

    try:
        bioview = Bio.objects.get(user_id = request.user.id)
    except:
        bioview =""
        
    try:
        location = Location.objects.get(user_id = request.user.id)
    except:
        location = ''

    

    Company = CustomUser.objects.filter(groups__name = "COMPANY")
    
    companies = CustomUser.objects.all()
    expertiselist =  Expertise.objects.filter(user_id = request.user.id)
    achievements = Achievements.objects.filter(user_id = request.user.id)
    projects = Projects.objects.filter(user_id = request.user.id)
    experiences = Experience.objects.filter(user_id = request.user.id)
    certificates = Certificate.objects.filter(user_id= request.user.id)
    testimonials = Testimonial.objects.filter(user_id = request.user.id)
    clients = Client.objects.filter(user_id = request.user.id)
    n = len(certificates)
    
    following_count = Follow2.objects.filter(following_id = request.user.id).count()
    follower_count = Follow2.objects.filter(follower_id = request.user.id).count()
    endorse_count = Endorse.objects.filter(liked_person_id =request.user.id).count()
    connection_count = Connection.objects.filter(Q(connected_person_id=request.user.id, connection=1) | Q(user_id=request.user.id, connection=1)).count()
   

    try:
        monview = Working.objects.get(day =1 ,user_id = request.user.id)
        
    except:
        monview = ''
        


    try:
        tueview = Working.objects.get(day =2,user_id = request.user.id )
        
    except:
        tueview = ''
        

    try:
        wedview = Working.objects.get(day =3, user_id = request.user.id)
        
    except:
        wedview = ''
        

    try:
        thuview = Working.objects.get(day =4,user_id = request.user.id )
       
    except:
        thuview = ''
        

    try:
        friview = Working.objects.get(day =5,user_id = request.user.id )
        
    except:
        friview = ''
        

    try:
        satview = Working.objects.get(day =6,user_id = request.user.id )
       
    except:
        satview = ''
        

    try:
        sunview = Working.objects.get(day =7,user_id = request.user.id )
        
    except:
        sunview = ''
        


    context = {
        'companies':companies,
        'userextend':userextend,
        'expertiselist':expertiselist,
        'achievements':achievements,
        'projects':projects,
        'experiences':experiences,
        'certificates':certificates,
        'testimonials':testimonials,
        'clients':clients,
        'monview': monview,
        'tueview': tueview,
        'wedview': wedview,
        'thuview': thuview,
        'friview': friview,
        'satview': satview,
        'sunview': sunview,
        'bioview':bioview,
        'Company':Company,
        'company':company,
        'location':location,
        'all_users': all_users,
        'all_img':all_img,
        
        'following_count':following_count,
        'follower_count':follower_count,
        'endorse_count':endorse_count,
        'connection_count':connection_count,
        'abouth':abouth,
        
        

    }

    return render(request,'profile/profile-user-edit.html',context)


@login_required(login_url = 'login')
def companyprofileview(request,id):
    
    company = request.user.groups.filter(name='COMPANY').exists()
    try:
        about = About.objects.get(user_id = id)
    except:
        about = ""
    is_following = Follow2.objects.filter(following_id=request.user.id, follower_id=id)
    instance = CustomUser.objects.get(id = id)
    userextend = UserExtend.objects.get(user_id=id)
    otheruser = int(id)
    otherusertb = CustomUser.objects.get(id= id)
    
    try:
        bioview = Bio.objects.get(user_id = id)
    except:
        bioview =""
        
    try:
        location = Location.objects.get(user_id = id)
    except:
        location = ''
        
    print(location)

    try:
        abouth = Aboutdetails.objects.get(user_id=request.user.id)
    except:
        abouth = ""



    expertiselist = Expertise.objects.filter(user_id=id)
    achievements = Achievements.objects.filter(user_id=id)
    projects = Projects.objects.filter(user_id=id)
    certificates = Certificate.objects.filter(user_id=id)
    clients = Client.objects.filter(user_id=id)
    branches = Branch.objects.filter(user_id=id)
    experiences = Experience.objects.filter(user_id=id)

    testimonial = Testimonial.objects.filter(user_id=id)
    
    following_count = Follow2.objects.filter(following_id = id).count()
    follower_count = Follow2.objects.filter(follower_id = id).count()
    endorse_count = Endorse.objects.filter(liked_person_id =id).count()
    connection_count = Connection.objects.filter(Q(connected_person_id=id, connection=1) | Q(user_id=id, connection=1)).count()
    
    is_following = Follow2.objects.filter(following_id = request.user.id, follower_id = id)
    endorse = Endorse.objects.filter(user_id = request.user.id, liked_person_id = id)
    if Connection.objects.filter(user_id = request.user.id, connected_person_id = id, connection = 0):
        is_connection = "requested"
        
    elif Connection.objects.filter(Q(connected_person_id=request.user.id, user_id=id, connection=1) | Q(user_id=request.user.id, connected_person_id=id, connection=1)):
        is_connection = "connected"
        
    else:
        is_connection = "notConnected"

    try:
        rating_view = Rating.objects.filter(rated_person = id).aggregate(Sum('rating'))
        rating_count = Rating.objects.filter(rated_person = id).count()
        e = (rating_view['rating__sum'])
        rating = e/rating_count
    except:
        rating = 0
    
    
    
    
    
    try:
        monview = Working.objects.get(day =1 ,user_id = id)
        
    except:
        monview = ''
        


    try:
        tueview = Working.objects.get(day =2,user_id = id )
        
    except:
        tueview = ''
       

    try:
        wedview = Working.objects.get(day =3, user_id = id)
        
    except:
        wedview = ''
        

    try:
        thuview = Working.objects.get(day =4,user_id = id )
        
    except:
        thuview = ''
       

    try:
        friview = Working.objects.get(day =5,user_id = id )
        
    except:
        friview = ''
        

    try:
        satview = Working.objects.get(day =6,user_id = id )
        
    except:
        satview = ''
        

    try:
        sunview = Working.objects.get(day =7,user_id = id )
        
    except:
        sunview = ''
        

    context = {
        'about':about,
        'expertiselist': expertiselist,
        'otheruser':otheruser,
        'otherusertb':otherusertb,
        'achievements': achievements,
        'projects': projects,
        'certificates': certificates,
        'clients': clients,
        'userextend':userextend,
        'branches': branches,
        'testimonial': testimonial,
        'experiences':experiences,
        'bioview':bioview,
        'monview': monview,
        'tueview': tueview,
        'wedview': wedview,
        'thuview': thuview,
        'friview': friview,
        'satview': satview,
        'sunview': sunview,
        'connection':is_following,
        'instance':instance,
        'company' :company,
        
        'following_count':following_count,
        'follower_count':follower_count,
        'endorse_count':endorse_count,
        'connection_count':connection_count,
        
        'connection':is_following,
        'endorse':endorse,
        'is_connection':is_connection,
        
        'location':location,
        'rating':rating,
        'abouth':abouth,
    }
    return  render(request,'profile/profile-company.html',context)


@login_required(login_url = 'login')
def userprofileview(request ,id):
    company = request.user.groups.filter(name='COMPANY').exists()
    otheruser = id
    otherusertb = CustomUser.objects.get(id= id)
    instance = CustomUser.objects.get(id=id)
    is_following = Follow2.objects.filter(following_id=request.user.id, follower_id=id)
    userextend = UserExtend.objects.get(user_id=id)
    try:
        bioview = Bio.objects.get(user_id = id)
    except:
        bioview =""
        
    try:
        location = Location.objects.get(user_id = id)
    except:
        location = ''

     #star rating view
    try:
        rating_view = Rating.objects.filter(rated_person = id).aggregate(Sum('rating'))
        rating_count = Rating.objects.filter(rated_person = id).count()
        e = (rating_view['rating__sum'])
        rating = e/rating_count
    except:
        rating = 0

    try:
        abouth = Aboutdetails.objects.get(user_id=id)
    except:
        abouth = ""

    expertiselist = Expertise.objects.filter(user_id=id)
    achievements = Achievements.objects.filter(user_id=id)
    projects = Projects.objects.filter(user_id=id)
    experiences = Experience.objects.filter(user_id=id)
    certificates = Certificate.objects.filter(user_id=id)
    testimonials = Testimonial.objects.filter(user_id=id)
    clients = Client.objects.filter(user_id=id)
    
    following_count = Follow2.objects.filter(following_id = id).count()
    follower_count = Follow2.objects.filter(follower_id = id).count()
    endorse_count = Endorse.objects.filter(liked_person_id =id).count()
    connection_count = Connection.objects.filter(Q(connected_person_id=id, connection=1) | Q(user_id=id, connection=1)).count()
    
    is_following = Follow2.objects.filter(following_id = request.user.id, follower_id = id)
    endorse = Endorse.objects.filter(user_id = request.user.id, liked_person_id = id)
    if Connection.objects.filter(user_id = request.user.id, connected_person_id = id, connection = 0):
        is_connection = "requested"
    elif Connection.objects.filter(Q(connected_person_id=request.user.id, user_id=id, connection=1) | Q(user_id=request.user.id, connected_person_id=id, connection=1)):
        is_connection = "connected"
    else:
        is_connection = "notConnected"
        
        
        
        
    try:
        monview = Working.objects.get(day =1 ,user_id =id)
       
    except:
        monview = ''
        


    try:
        tueview = Working.objects.get(day =2,user_id = id )
        
    except:
        tueview = ''
      

    try:
        wedview = Working.objects.get(day =3, user_id = id)
        
    except:
        wedview = ''
        

    try:
        thuview = Working.objects.get(day =4,user_id = id )
       
    except:
        thuview = ''
       

    try:
        friview = Working.objects.get(day =5,user_id = id )
        
    except:
        friview = ''
       

    try:
        satview = Working.objects.get(day =6,user_id = id )
        
    except:
        satview = ''
        

    try:
        sunview = Working.objects.get(day =7,user_id = id )
       
    except:
        sunview = ''

    try:
        abouth = Aboutdetails.objects.get(user_id=id)
    except:
        abouth = ""
       

    context = {

        'expertiselist': expertiselist,
        'userextend':userextend,
        'otheruser':otheruser,
        'achievements': achievements,
        'projects': projects,
        'experiences': experiences,
        'certificates': certificates,
        'testimonials': testimonials,
        'otherusertb':otherusertb,

        'clients': clients,
        'bioview':bioview,
        'monview': monview,
        'tueview': tueview,
        'wedview': wedview,
        'thuview': thuview,
        'friview': friview,
        'satview': satview,
        'sunview': sunview,
        'connection': is_following,
        'instance': instance,
        'company':company,
        
        'following_count':following_count,
        'follower_count':follower_count,
        'endorse_count':endorse_count,
        'connection_count':connection_count,
        
        'connection':is_following,
        'endorse':endorse,
        'is_connection':is_connection,
        
        'location':location,
        'rating':rating,
        'abouth':abouth,
        
        
        

    }
    return  render(request,'profile/profile-user.html',context)


@login_required(login_url = 'login')
def experience(request):
    return render(request,'profile/experience.html')

@login_required(login_url = 'login')
def experiencelist(request,id):
    experiences = Experience.objects.filter(user_id = id)
    context = {
        'experiences':experiences,
    }
    return render(request,'profile/experiencelist.html',context)


##############adding working hours #############

@login_required(login_url = 'login')
def addworking(request):

    try:

        
        mondview = Working.objects.get(user_id=request.user.id,day = 1)

        

        if request.method == "POST":
            Moncheck = request.POST.get('moncheck')
            Monstart = request.POST.get('monstartime')

            Monend = request.POST.get('monendtime')
            MonBrk1st = request.POST.get('monbreaktime1st')
            MonBrk1en = request.POST.get('monbreaktime1en')
            MonBrk2st = request.POST.get('monbreaktime2st')
            MonBrk2en = request.POST.get('monbreaktime2en')

            mondview.start_time = Monstart
            mondview.end_time = Monend
            mondview.breaktimef_start = MonBrk1st
            mondview.breaktimef_end = MonBrk1en
            mondview.breaktimes_start = MonBrk2st
            mondview.breaktimes_end = MonBrk2en
            mondview.day = 1
            mondview.save()

    except:
        

        Moncheck = request.POST.get('moncheck')
        Monstart = request.POST.get('monstartime')
        Monend =    request.POST.get('monendtime')
        MonBrk1st = request.POST.get('monbreaktime1st')
        MonBrk1en = request.POST.get('monbreaktime1en')
        MonBrk2st = request.POST.get('monbreaktime2st')
        MonBrk2en = request.POST.get('monbreaktime2en')



        if request.method == "POST":
            if Moncheck:
                working = Working()
                working.start_time = Monstart
                working.end_time = Monend
                working.breaktimef_start = MonBrk1st
                working.breaktimef_end = MonBrk1en
                working.breaktimes_start = MonBrk2st
                working.breaktimes_end = MonBrk2en
                working.day = 1
                working.user_id = request.user.id
                working.save()
                


    try:

        tueview = Working.objects.get(user_id=request.user.id, day=2)
        

        if request.method == "POST":
            Tuecheck = request.POST.get('tuecheck')
            Tuestart = request.POST.get('tuestartime')
            Tueend = request.POST.get('tueendtime')
            TueBrk1st = request.POST.get('tuebreaktime1st')
            TueBrk1en = request.POST.get('tuebreaktime1en')
            TueBrk2st = request.POST.get('tuebreaktime2st')
            TueBrk2en = request.POST.get('tuebreaktime2en')

            tueview.start_time = Tuestart
            tueview.end_time = Tueend
            tueview.breaktimef_start = TueBrk1st
            tueview.breaktimef_end = TueBrk1en
            tueview.breaktimes_start = TueBrk2st
            tueview.breaktimes_end = TueBrk2en
            tueview.day = 2
            tueview.save()

    except:
        
        if request.method == "POST":
            Tuecheck = request.POST.get('tuecheck')
            Tuestart = request.POST.get('tuestartime')
            Tueend = request.POST.get('tueendtime')
            TueBrk1st = request.POST.get('tuebreaktime1st')
            TueBrk1en = request.POST.get('tuebreaktime1en')
            TueBrk2st = request.POST.get('tuebreaktime2st')
            TueBrk2en = request.POST.get('tuebreaktime2en')
            if Tuecheck:
                working = Working()
                working.start_time = Tuestart
                working.end_time = Tueend
                working.breaktimef_start = TueBrk1st
                working.breaktimef_end = TueBrk1en
                working.breaktimes_start = TueBrk2st
                working.breaktimes_end = TueBrk2en
                working.day = 2
                working.user_id = request.user.id
                working.save()
                


            

    try:
        wedview = Working.objects.get(user_id=request.user.id, day=3)
       

        if request.method == "POST":
            Wedcheck = request.POST.get('wedcheck')
            Wedstart = request.POST.get('wedstartime')
            Wedend = request.POST.get('wedendtime')
            WedBrk1st = request.POST.get('wedbreaktime1st')
            WedBrk1en = request.POST.get('wedbreaktime1en')
            WedBrk2st = request.POST.get('wedbreaktime2st')
            WedBrk2en = request.POST.get('wedbreaktime2en')

            wedview.start_time = Wedstart
            wedview.end_time = Wedend
            wedview.breaktimef_start = WedBrk1st
            wedview.breaktimef_end = WedBrk1en
            wedview.breaktimes_start = WedBrk2st
            wedview.breaktimes_end = WedBrk2en
            wedview.day = 3
            wedview.save()

    except:
        

        if request.method == "POST":
            Wedcheck = request.POST.get('wedcheck')
            Wedstart = request.POST.get('wedstartime')
            Wedend = request.POST.get('wedendtime')
            WedBrk1st = request.POST.get('wedbreaktime1st')
            WedBrk1en = request.POST.get('wedbreaktime1en')
            WedBrk2st = request.POST.get('wedbreaktime2st')
            WedBrk2en = request.POST.get('wedbreaktime2en')
            if Wedcheck:
                working = Working()
                working.start_time = Wedstart
                working.end_time = Wedend
                working.breaktimef_start = WedBrk1st
                working.breaktimef_end = WedBrk1en
                working.breaktimes_start = WedBrk2st
                working.breaktimes_end = WedBrk2en
                working.day = 3
                working.user_id = request.user.id
                working.save()
                

    try:
        thuview = Working.objects.get(user_id=request.user.id, day=4)
        

        if request.method == "POST":
            Thucheck = request.POST.get('thucheck')
            Thustart = request.POST.get('thustartime')
            Thuend = request.POST.get('thuendtime')
            ThuBrk1st = request.POST.get('thubreaktime1st')
            ThuBrk1en = request.POST.get('thubreaktime1en')
            ThuBrk2st = request.POST.get('thubreaktime2st')
            ThuBrk2en = request.POST.get('thubreaktime2en')

            thuview.start_time = Thustart
            thuview.end_time = Thuend
            thuview.breaktimef_start = ThuBrk1st
            thuview.breaktimef_end = ThuBrk1en
            thuview.breaktimes_start = ThuBrk2st
            thuview.breaktimes_end = ThuBrk2en
            thuview.day = 4
            thuview.save()

    except:
        

        if request.method == "POST":
            Thucheck = request.POST.get('thucheck')
            Thustart = request.POST.get('thustartime')
            Thuend = request.POST.get('thuendtime')
            ThuBrk1st = request.POST.get('thubreaktime1st')
            ThuBrk1en = request.POST.get('thubreaktime1en')
            ThuBrk2st = request.POST.get('thubreaktime2st')
            ThuBrk2en = request.POST.get('thubreaktime2en')
            if Thucheck:
                working = Working()
                working.start_time = Thustart
                working.end_time = Thuend
                working.breaktimef_start = ThuBrk1st
                working.breaktimef_end = ThuBrk1en
                working.breaktimes_start = ThuBrk2st
                working.breaktimes_end = ThuBrk2en
                working.day = 4
                working.user_id = request.user.id
                working.save()
                

    try:
        friview = Working.objects.get(user_id=request.user.id, day=5)
       

        if request.method == "POST":
            Fricheck = request.POST.get('fricheck')
            Fristart = request.POST.get('fristartime')
            Friend = request.POST.get('friendtime')
            FriBrk1st = request.POST.get('fribreaktime1st')
            FriBrk1en = request.POST.get('fribreaktime1en')
            FriBrk2st = request.POST.get('fribreaktime2st')
            FriBrk2en = request.POST.get('fribreaktime2en')

            friview.start_time = Fristart
            friview.end_time = Friend
            friview.breaktimef_start = FriBrk1st
            friview.breaktimef_end = FriBrk1en
            friview.breaktimes_start = FriBrk2st
            friview.breaktimes_end = FriBrk2en
            friview.day = 5
            friview.save()

    except:
        

        if request.method == "POST":
            Fricheck = request.POST.get('fricheck')
            Fristart = request.POST.get('fristartime')
            Friend = request.POST.get('friendtime')
            FriBrk1st = request.POST.get('fribreaktime1st')
            FriBrk1en = request.POST.get('fribreaktime1en')
            FriBrk2st = request.POST.get('fribreaktime2st')
            FriBrk2en = request.POST.get('fribreaktime2en')
            if Fricheck:
                working = Working()
                working.start_time = Fristart
                working.end_time = Friend
                working.breaktimef_start = FriBrk1st
                working.breaktimef_end = FriBrk1en
                working.breaktimes_start = FriBrk2st
                working.breaktimes_end = FriBrk2en
                working.day = 5
                working.user_id = request.user.id
                working.save()
                

    try:
        satview = Working.objects.get(user_id=request.user.id, day=6)
        

        if request.method == "POST":
            Satcheck = request.POST.get('satcheck')
            Satstart = request.POST.get('satstartime')
            Satend = request.POST.get('satendtime')
            SatBrk1st = request.POST.get('satbreaktime1st')
            SatBrk1en = request.POST.get('satbreaktime1en')
            SatBrk2st = request.POST.get('satbreaktime2st')
            SatBrk2en = request.POST.get('satbreaktime2en')

            satview.start_time =Satstart
            satview.end_time = Satend
            satview.breaktimef_start = SatBrk1st
            satview.breaktimef_end = SatBrk1en
            satview.breaktimes_start = SatBrk2st
            satview.breaktimes_end = SatBrk2en
            satview.day = 6
            satview.save()

    except:
        

        if request.method == "POST":
            Satcheck = request.POST.get('satcheck')


            Satstart = request.POST.get('satstartime')
            Satend = request.POST.get('satendtime')
            SatBrk1st = request.POST.get('satbreaktime1st')
            SatBrk1en = request.POST.get('satbreaktime1en')
            SatBrk2st = request.POST.get('satbreaktime2st')
            SatBrk2en = request.POST.get('satbreaktime2en')
            if Satcheck:
                working = Working()
                working.start_time = Satstart
                working.end_time = Satend
                working.breaktimef_start = SatBrk1st
                working.breaktimef_end = SatBrk1en
                working.breaktimes_start = SatBrk2st
                working.breaktimes_end = SatBrk2en
                working.day = 6
                working.user_id = request.user.id
                working.save()
               

    try:
        sunview = Working.objects.get(user_id=request.user.id, day=7)
        

        if request.method == "POST":
            Suncheck = request.POST.get('suncheck')
            Sunstart = request.POST.get('sunstartime')
            Sunend = request.POST.get('sunendtime')
            SunBrk1st = request.POST.get('sunbreaktime1st')
            SunBrk1en = request.POST.get('sunbreaktime1en')
            SunBrk2st = request.POST.get('sunbreaktime2st')
            SunBrk2en = request.POST.get('sunbreaktime2en')

            sunview.start_time =Sunstart
            sunview.end_time = Sunend
            sunview.breaktimef_start = SunBrk1st
            sunview.breaktimef_end = SunBrk1en
            sunview.breaktimes_start = SunBrk2st
            sunview.breaktimes_end = SunBrk2en
            sunview.day = 7
            sunview.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except:

       

        if request.method == "POST":
            Suncheck = request.POST.get('suncheck')
            Sunstart = request.POST.get('sunstartime')
            Sunend = request.POST.get('sunendtime')
            SunBrk1st = request.POST.get('sunbreaktime1st')
            SunBrk1en = request.POST.get('sunbreaktime1en')
            SunBrk2st = request.POST.get('sunbreaktime2st')
            SunBrk2en = request.POST.get('sunbreaktime2en')
            if Suncheck:
                working = Working()
                working.start_time = Sunstart
                working.end_time = Sunend
                working.breaktimef_start = SunBrk1st
                working.breaktimef_end = SunBrk1en
                working.breaktimes_start = SunBrk2st
                working.breaktimes_end = SunBrk2en
                working.day = 7
                working.user_id = request.user.id
                working.save()
                




        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = 'login')
def transalator(request):
    if request.method == "POST":
        text = request.POST.get('texts')
       
        
        
        
        
        
        phone_number1 = phonenumbers.parse(text)
        
        
        
        phone_number2 = phonenumbers.parse(text)
        


    return render(request,'transalator.html')

@login_required(login_url = 'login')
def aboutus(request):
    form = AboutForm
    if request.method== "POST":
        form = AboutForm(request.POST)
        about = form.save(commit = False)
        about.user_id = request.user.id
        about.save()
    return render(request, 'profile/profile-company-edit.html')

@login_required(login_url = 'login')
def achievements(request):
    AchievementFormSet = modelformset_factory(Achievement, fields=('name',), extra=3)

    if request.method == "POST":
        formset = AchievementFormSet(request.POST)
        instances = formset.save(commit=False)

        for instance in instances:
            instance.user_id = request.user.id
            instance.save()

    formset = AchievementFormSet(queryset = Achievement.objects.filter(user_id = request.user.id))

    context = {'formset': formset}

    return render(request, 'profile/profile-company-edit.html',context)

@login_required(login_url = 'login')
def addlocation(request):
    try:
        
        location = Location.objects.get(user_id = request.user.id )
        
        if request.method == "POST":
            locat= request.POST.get('location') 
            
            location.place = locat
            location.user_id = request.user.id
            location.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        
        if request.method == "POST":
            
            location = request.POST.get('location') 
            loc = Location()
            loc.place = location
            loc.user_id = request.user.id
            loc.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
    

@login_required(login_url = 'login')
def projects(request):
    form = ProjectsForm()
    if request.method == "POST":
        form = ProjectsForm(request.POST)
        productname = request.POST.get('project_name')
        company = request.POST.get('company_name')
        authority = request.POST.get('company_name_id')
        if authority:
            auth = int(authority)
        
        projects = Projects()
        projects.user_id = request.user.id
        projects.authname = company 
        projects.project_name = productname
        if authority:
            projects.auth_id = auth   
            
        projects.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def editprojects(request,id):
    pro = Projects.objects.get(id = id)
    if request.method == "POST":
        Proj = request.POST.get('project_name')
        Comp = request.POST.get('company_name_edit')
        authority = request.POST.get('company_name_edit_id')
        if authority:
            autho = int(authority)
        pro.authname = Comp
        
        pro.project_name = Proj
        if authority:
            pro.auth_id = autho
        pro.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url = 'login')
def cexpertise(request):
    CexpertiseFormset = modelformset_factory(Cexepertise,fields = ('profession','year'),extra = 3)
    if request.method == "POST":
        cexpertiseForm = CexpertiseFormset(request.POST)
        instances = cexpertiseForm(commit = False)
        for instance in instances:
            instance.user_id = request.user.id
            instance.save()
    cexpertiseForm = CexpertiseFormset(queryset = Cexepertise.objects.filter(user_id = request.user.id))
    context = {
        'cexpertiseForm':cexpertiseForm
    }
    return render(request, 'profile/profile-company-edit.html', context)


@csrf_exempt
@login_required(login_url = 'login')
def addabout(request):
    try:

        a = 1
        
        view = About.objects.get(user_id =request.user.id )
        form = AboutForm(instance = view)
        if request.method == "POST":
            form = AboutForm(request.POST,instance = view)
            if form.is_valid():
                z = form.save()
                ser_instance = serializers.serialize('json', [z, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)



    except:

        a = 2
        
        form = AboutForm()
        if request.method == "POST":
            form = AboutForm(request.POST or None)
            if form.is_valid():
                form = AboutForm(request.POST)
                about = form.save(commit=False)
                about.user_id = request.user.id
                about.save()
                return  HttpResponse('added')
            else:
                return HttpResponse('invalid')

    return JsonResponse({"error": ""}, status=400)


@login_required(login_url = 'login')
def expertise(request):
    
    form = ExpertiseForm()
    if request.method == "POST":
        
        exp = request.POST.get('expertise')
        expid = request.POST.get('expertise_id')
        form = ExpertiseForm(request.POST)
        if form.is_valid():
            experti  = form.save(commit = False)
            experti.user_id = request.user.id
            experti.authname = exp
            if expid:
                experti.auth_id = expid
            experti.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = 'login')
def editexpertise(request,id):
    exp = Expertise.objects.get(id = id)
    expedit = request.POST.get('expertise_edit')
    expid = request.POST.get('expertise_edit_id')
    
    print(expedit,expid)
    if request.method == "POST":
        a = request.POST.get('profession')
        b = request.POST.get('expertisein')
        c = request.POST.get('years')
        d = request.POST.get('description')
        exp.profession = a
        exp.expertisein = b
        exp.years = c
        exp.description = d
        if expid:
            exp.auth_id = expid
        exp.authname = expedit 
        exp.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required(login_url = 'login')
def addachievements(request):
    form  = AchievementsForm()
    if request.method == "POST":
        form = AchievementsForm(request.POST)
        ach = request.POST.get('achievementss')
        achid = request.POST.get('achievementss_id')
        if achid:
            achi = int(achid)
        if form.is_valid():
            achievement = form.save(commit = False)
            achievement.user_id = request.user.id
            achievement.authname = ach
            if achid:
                achievement.auth_id = achi
            achievement.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def editachievements(request,id):
    ach = Achievements.objects.get(id= id)
    if request.method == "POST":
        tit = request.POST.get('achievementtitle')
        ache = request.POST.get('achievementss_edit')
        achid = request.POST.get('achievementss_edit_id')
        
        
        des = request.POST.get('description')
        
        if achid:
            achi = int(achid)
            ach.auth_id = achi
        ach.authname = ache
        ach.description= des
        ach.title = tit
        ach.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required(login_url = 'login')
def experience(request):
    form = ExperienceForm()
    if request.method == "POST":
        companyid = request.POST.get('company-name_id')
        companyname = request.POST.get('company-name')
        
        company = request.POST.get('company')
        if companyid:
            cid = int(companyid)
        form = ExperienceForm(request.POST,request.FILES)
        if form.is_valid():
            exp = form.save(commit = False)
            exp.user_id = request.user.id
            exp.company_name = companyname
            if companyid:
                exp.company_id = cid
            exp.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def editexperience(request,id):
    exp = Experience.objects.get(id = id)
    if request.method == "POST":
        fromyear = request.POST.get('fromyear')
        toyear = request.POST.get('toyear')
        companyname = request.POST.get('company-name_edit')
        
        company_id = request.POST.get('client-name_edit_id')
        if company_id:
            cid = int(companyname)
        exp_keywords = request.POST.get('exp_keywords')
        expdetail = request.POST.get('exp_detail')
        comments = request.POST.get('comments')
        responsibility = request.POST.get('responsibility')
        expimage = request.POST.get('expimage')

        exp.fromyear = fromyear
        if company_id:
            exp.company_id = cid
        exp.company_name = companyname
        exp.toyear = toyear
        exp.exp_keywords = exp_keywords
        exp.exp_detail = expdetail
        exp.comments = comments
        exp.responsibily = responsibility
        exp.expimage = expimage
        exp.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def addclient(request):
    form = ClientForm()
    if request.method == "POST":
        ClientName = request.POST.get('client-name')
        Client = request.POST.get('client-name_id')
        Img = request.FILES.get('clientImage')
        if Client:
            c= int(Client)
        form = ClientForm(request.POST,request.FILES)
        if form.is_valid():
            client = form.save(commit = False)
            client.user_id = request.user.id
            client.clientname = ClientName
            if Img:
                client.clientimage = Img
            if Client:
                client.client_id = c
            client.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def editclient(request,id):
    cli = Client.objects.get(id = id)
    if request.method == "POST":
        ClientName = request.POST.get('client-name_edit')
        Cliid = request.POST.get('client-name_edit_id')
        Cliimage = request.FILES.get('clientimage')
        Clidesc = request.POST.get('client_description')


        
        if Cliid:
            cid = int(Cliid)
            cli.client_id = cid
        if Cliimage:
            cli.clientimage = Cliimage
        else:
            pass
        cli.client_description = Clidesc
        cli.clientname = ClientName
        cli.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url = 'login')
def addtestimonial(request):
    form = TestimonialForm()
    if request.method == "POST":
        Test = request.POST.get('testicliName')
        Testid = request.POST.get('testicliName-id')
        
        
        form = TestimonialForm(request.POST,request.FILES)
        if form.is_valid():
            testimonial = form.save(commit = False)
            
            testimonial.user_id = request.user.id
            testimonial.testimonial_name = Test
            if Testid:
                d =int(Testid)
                
                testimonial.testuser_id = d
            testimonial.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = 'login')
def edittestimonial(request,id):
    test = Testimonial.objects.get(id = id)
    if request.method == "POST":
        Test = request.POST.get('testicliNameEdit')
        Testid = request.POST.get('testicliName-idEdit{{i.id}}')
        TestImg = request.FILES.get('testimonial_image')
        Testdesc = request.POST.get('testimonial_description')

        
       
        test.testimonial_name = Test

        if TestImg:
            test.testimonial_image = TestImg
        else:
            pass
        
        if Testid:
            Clname = int(Testid)
            test.testuser_id = Clname
        test.testimonial_description = Testdesc
        test.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = 'login')
def addcertificate(request):
    form = CertificateForm()
    if request.method == "POST":
        AuthorityName = request.POST.get('issued_authority')
        Authority = request.POST.get('issued_authority_id')
        
        
        if Authority:
            a = int(Authority)

       
        form = CertificateForm(request.POST,request.FILES)
        if form.is_valid():
            certificate = form.save(commit = False)
            certificate.user_id = request.user.id
            if Authority:
                certificate.authority_id = a
            certificate.company_name = AuthorityName
            certificate.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def editcertificate(request,id):
    
    cer = Certificate.objects.get(id = id)
    if request.method == "POST":
        isauth = request.POST.get('issued_authority_edit_id')
        authname = request.POST.get('issued_authority_edit')
        Cername = request.POST.get('certificate_name')
        CerId = request.POST.get('certificate_id')
        CerIma = request.FILES.get('certificate_image')
        CerDes = request.POST.get('certificate_description')
       


       
        if isauth :
            IA = int(isauth)
            
        if isauth :
            cer.authority_id  = IA
        cer.certificate_name = Cername
        
        cer.certificate_id = CerId
        cer.company_name = authname

        if CerIma:
            cer.certificate_image = CerIma
        else:
            pass
        cer.certificate_description = CerDes



        cer.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def  addbranch(request):
    form = BranchForm()
    if request.method == "POST":
        form = BranchForm(request.POST,request.FILES)
        if form.is_valid():
            certificate = form.save(commit = False)
            certificate.user_id = request.user.id
            certificate.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = 'login')
def editbranch(request,id):

    branch = Branch.objects.get(id = id)
    if request.method == "POST":
            branchP = request.POST.get('branch')
            branchAddres = request.POST.get('branchaddress')

            branch.branch= branchP
            branch.branchaddress = branchAddres
            branch.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




######################################CERTIFICATE verification ##################################
@login_required(login_url = 'login')
def verifycertificate(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    
    pending = Certificate.objects.filter(authority_id = request.user.id ,is_requested = 1,is_approved = 0,is_rejected = 0)
    approved = Certificate.objects.filter(authority_id = request.user.id,is_requested = 1,is_approved = 1,is_rejected = 0)
    companies = CustomUser.objects.all()
    
    context = {
        'pending':pending,
        'approved':approved,
        'companies':companies,
        'company':company,
    }
    return render(request,'verification/verification-certificate.html',context)

@login_required(login_url = 'login')
def approvecertificate(request,id):
    
    approve = Certificate.objects.get(id = id)
    approve.is_approved = 1
    approve.save()

    Cer = approve.authority_id

    notify = Notification()
    notify.user_id = request.user.id
    notify.sender_id = Cer
    notify.notification_type = 3
    notify.save()
    return redirect('verifycertificate')

@login_required(login_url = 'login')
def deletecertificate(request,id):
    dele = Certificate.objects.get(id = id)
    dele.is_rejected = 1
    dele.save()
    
    return redirect('verifycertificate')

@login_required(login_url = 'login')
def editverificationcertificate(request,id):
    cer = Certificate.objects.get(id = id)
    if request.method == "POST":
        Cername = request.POST.get('certificate_name')
        CerId = request.POST.get('certificate_id')
        CerIma = request.FILES.get('certificate_image')
        CerDes = request.POST.get('certificate_description')

        
        cer.certificate_name = Cername
        cer.certificate_id = CerId
        if CerIma:
            cer.certificate_image = CerIma
        else:
            pass

        cer.certificate_description = CerDes
        cer.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def sendvercertificate(request,id):

    sendreq = Certificate.objects.get(id = id)
    sendreq.is_requested = 1
    sendreq.save()




   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




###################CLIENT verification ######################################
@login_required(login_url = 'login')
def verifyclient(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    pending = Client.objects.filter(client_id = request.user.id ,is_requested = 1,is_approved = 0,is_rejected = 0)
    approved = Client.objects.filter(client_id = request.user.id ,is_requested = 1,is_approved = 1,is_rejected = 0)
    context = {
        'pending': pending,
        'approved': approved,
        'company':company
    }
    return render(request, 'verification/verification-client.html',context)


@login_required(login_url = 'login')
def approveclient(request,id):
    approve = Client.objects.get(id = id)
    approve.is_approved = 1
    approve.save()
    return redirect('verifyclient')

@login_required(login_url = 'login')
def deleteclient(request,id):
    dele = Client.objects.get(id = id)
    dele.is_rejected = 1
    dele.save()
    return redirect('verifyclient')

@login_required(login_url = 'login')
def editverificationclient(request,id):
    cli = Client.objects.get(id = id)

    if request.method == "POST":

        # Cliid = request.POST.get('client-name')
        Cliimage = request.FILES.get('clientimage')
        Clidesc = request.POST.get('client_description')

        
        cli.client_description = Clidesc
        if Cliimage:



            cli.clientimage = Cliimage
        else:
            pass
        cli.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def sendverclient(request,id):
    sendreq = Client.objects.get(id = id)
    sendreq.is_requested = 1
    sendreq.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#####################TESTIMONIAL Verification ######################################

@login_required(login_url = 'login')
def verifytestimonial(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    pending = Testimonial.objects.filter(testuser_id=request.user.id,is_requested = 1, is_approved=0,is_rejected = 0)
    approved = Testimonial.objects.filter(testuser_id=request.user.id,is_requested = 1, is_approved=1,is_rejected = 0)
    context = {
        'pending': pending,
        'approved': approved,
        'company':company,
    }
    return render(request, 'verification/verification-testimonial.html',context)


@login_required(login_url = 'login')
def approvetestimonial(request,id):
    approve = Testimonial.objects.get(id = id)
    approve.is_approved = 1
    approve.save()
    return redirect('verifytestimonial')

@login_required(login_url = 'login')
def deletetestimonial(request,id):
    dele = Testimonial.objects.get(id = id)
    dele.is_rejected = 1
    dele.save()
    return redirect('verifytestimonial')

@login_required(login_url = 'login')
def editverificationtestimonial(request,id):
    testi = Testimonial.objects.get(id = id)

    if request.method == "POST":
        TestImg = request.FILES.get('testimonial_image')
        Testdesc = request.POST.get('testimonial_description')

        testi.testimonial_description = Testdesc

       

        if TestImg:
            testi.testimonial_image = TestImg
        else:
            pass
        testi.save()



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def sendvertestimonial(request,id):
    
    sendreq = Testimonial.objects.get(id = id)
    sendreq.is_requested = 1
    sendreq.save()
   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

###########################verify achievement######################

@login_required(login_url = 'login')
def verifyachievements(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    pending = Achievements.objects.filter(auth_id= request.user.id,is_requested = 1, is_approved=0,is_rejected = 0)
    approved = Achievements.objects.filter(auth_id= request.user.id,is_requested = 1, is_approved=1,is_rejected = 0)
    
    
    context = {
        'pending': pending,
        'approved': approved,
        'company':company,
    }
    return render(request, 'verification/verification-achievements.html',context)

@login_required(login_url = 'login')
def approveachievements(request,id):
    approve = Achievements.objects.get(id = id)
    approve.is_approved = 1
    approve.save()
    return redirect('verifyachievements')

@login_required(login_url = 'login')
def deleteachievements(request,id):
    dele = Achievements.objects.get(id = id)
    dele.is_rejected = 1
    dele.save()
    return redirect('verifytestimonial')

@login_required(login_url = 'login')
def editverificationachievements(request,id):
    testi = Achievements.objects.get(id = id)

    if request.method == "POST":
        # TestImg = request.FILES.get('testimonial_image')
        Achtitle = request.POST.get('achtitle')
        AchDesc = request.POST.get('achdesc')

        testi.title = Achtitle
        testi.description = AchDesc

       

        # if TestImg:
        #     testi.testimonial_image = TestImg
        # else:
        #     pass
        testi.save()



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def sendverachievements(request,id):
    
    sendreq = Achievements.objects.get(id = id)
    sendreq.is_requested = 1
    sendreq.save()
   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#########################verify expertise###########################

@login_required(login_url = 'login')
def verifyexpertise(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    pending = Expertise.objects.filter(auth_id=request.user.id,is_requested = 1, is_approved=0,is_rejected = 0)
    approved = Expertise.objects.filter(auth_id=request.user.id,is_requested = 1, is_approved=1,is_rejected = 0)
    

    context = {
        'pending': pending,
        'approved': approved,
        'company':company,
    }
    return render(request, 'verification/verification-expertise.html',context)

@login_required(login_url = 'login')
def approveexpertise(request,id):
    approve = Expertise.objects.get(id = id)
    approve.is_approved = 1
    approve.save()
    return redirect('verifyexpertise')

@login_required(login_url = 'login')
def deleteexpertise(request,id):
    dele = Expertise.objects.get(id = id)
    dele.is_rejected = 1
    dele.save()
    return redirect('verifyexpertise')

@login_required(login_url = 'login')
def editverificationexpertise(request,id):
    testi = Expertise.objects.get(id = id)

    if request.method == "POST":
        exprofession = request.POST.get('exprofession')
        expexpertisein = request.POST.get('expexpertisein')
        expyears = request.POST.get('expyears')
        expdescription = request.POST.get('expdescription')
        
        
        testi.profession = exprofession
        testi.expertisein = expexpertisein
        testi.years = expyears
        testi.description = expdescription
        
        testi.save()



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def sendverexpertise(request,id):
    
    sendreq = Expertise.objects.get(id = id)
    sendreq.is_requested = 1
    sendreq.save()
   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#########################verify projects##########################

@login_required(login_url = 'login')
def verifyprojects(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    pending = Projects.objects.filter(auth_id=request.user.id,is_requested = 1, is_approved=0,is_rejected = 0)
    approved = Projects.objects.filter(auth_id=request.user.id,is_requested = 1, is_approved=1,is_rejected = 0)
    
    context = {
        'pending': pending,
        'approved': approved,
        'company':company,
    }
    return render(request, 'verification/verification-projectsproducts.html',context)

@login_required(login_url = 'login')
def approveprojects(request,id):
    approve = Projects.objects.get(id = id)
    approve.is_approved = 1
    approve.save()
    return redirect('verifyprojects')

@login_required(login_url = 'login')
def deleteprojects(request,id):
    dele = Projects.objects.get(id = id)
    dele.is_rejected = 1
    dele.save()
    return redirect('verifyprojects')

@login_required(login_url = 'login')
def editverificationprojects(request,id):
    testi = Projects.objects.get(id = id)

    if request.method == "POST":
        
        projectname = request.POST.get('projectname')

        testi.project_name = projectname
        testi.save()



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def sendverprojects(request,id):
    sendreq = Projects.objects.get(id = id)
    sendreq.is_requested = 1
    sendreq.save()
   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

##########################verify experience ##############

@login_required(login_url = 'login')
def verifyexperience(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    pending = Experience.objects.filter(company_id=request.user.id,is_requested = 1, is_approved=0,is_rejected = 0)
    approved = Experience.objects.filter(company_id=request.user.id,is_requested = 1, is_approved=1,is_rejected = 0)

    context = {
        'pending': pending,
        'approved': approved,
        'company':company,
    }
    return render(request, 'verification/verification-experience.html',context)

@login_required(login_url = 'login')
def approveexperience(request,id):
    approve = Experience.objects.get(id = id)
    approve.is_approved = 1
    approve.save()
    return redirect('verifyexperience')

@login_required(login_url = 'login')
def deleteexperience(request,id):
    dele = Experience.objects.get(id = id)
    dele.is_rejected = 1
    dele.save()
    return redirect('verifyexperience')

@login_required(login_url = 'login')
def editverificationexperience(request,id):
    testi = Experience.objects.get(id = id)

    if request.method == "POST":
        fromyear = request.POST.get('fromyear')
        toyear = request.POST.get('toyear')
        
        
        exp_keywords = request.POST.get('exp_keywords')
        expdetail = request.POST.get('exp_detail')
        comments = request.POST.get('comments')
        responsibility = request.POST.get('responsibility')
        
        testi.fromyear = fromyear
        testi.toyear = toyear
        testi.exp_keywords = exp_keywords
        testi.exp_detail = expdetail
        testi.comments = comments
        testi.responsibily = responsibility

        testi.save()



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def sendverxperience(request,id):
    
    sendrequ = Experience.objects.get(id = id)
    sendrequ.is_requested = 1
    sendrequ.save()
   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

############################SHARE####################

@login_required(login_url = 'login')
def share(request):

    broushers = Brousher.objects.filter(user_id = request.user.id)
    cards = Cards.objects.filter( user_id = request.user.id )
    images = Image.objects.filter(user_id = request.user.id)

    try:
        bioview = Bio.objects.get(user_id = request.user.id)
    except:
        bioview =""

    context = {
        'bioview':bioview,
        'broushers':broushers,
        'cards':cards,
        'images':images,
    }
    return render(request,'share/share.html',context)

@login_required(login_url = 'login')
def addbrousher(request):

    if request.method == "POST":
        Brousherimage = request.FILES.get('file')
        brousher = Brousher()
        brousher.brousher = Brousherimage
        brousher.user_id = request.user.id
        brousher.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def addcard(request):
    if request.method == "POST":
        Cardimg = request.FILES.get('file')
        cards = Cards()
        cards.card = Cardimg
        cards.user_id = request.user.id
        cards.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def addimage(request):
    if request.method == "POST":
        Img = request.FILES.get('file')
        img = Image()
        img.image = Img
        img.user_id = request.user.id
        img.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def adddocs(request):
    if request.method == "POST":
        DOC = request.FILES.get('file')
        doc = Documents()
        doc.DOCS = DOC
        doc.user_id = request.user.id
        doc.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def postreport(request):
    postitems = Post.objects.all()
    print(postitems)
    context = {
        'postitems':postitems,
    }
    return render(request,'panel/postreport.html',context)




#################jquery company name autocomplete####################


# def company_autocomplete(request):
#     if 'term' in request.GET:
#         qs = UserExtend.objects.filter(company_name__istartswith = request.GET.get('term'))
#         names = []
#
#         for company in qs:
#             names.append(company.company_name)
#         return JsonResponse(names,safe = False)
#     return render(request,'profile/profile-user-edit.html')


def company_autocomplete(request):
    if 'term' in request.GET:
        qs = UserExtend.objects.filter(company_name__istartswith = request.GET.get('term'))
        names = []

        for company in qs:
            names.append({'label':company.company_name, 'value':company.user_id})
        return HttpResponse(json.dumps(names), content_type='application/json')
    # return render(request,'profile/profile-user-edit.html')

def client_autocomplete(request):
    if 'term' in request.GET:
        qs = CustomUser.objects.filter(email__istartswith = request.GET.get('term'))
        # qsc = UserExtend.objects.filter(company_name__istartswith = request.GET.get('term'))
        
        names = []

        for company in qs:
            #pofilepics = json.dumps(str(company.bio.image))
           
            p = company.bio.address 
            fn = company.first_name 
            ln  = company.last_name 
            print(p)
            
            if ln == None:
                ln = ''
            else:
                ln = ln
            
            if p == None :
    
                p = ''
            else:
                p = p
            
            print(p)
            print(fn,ln)
            
            name = fn + ' ' + ln + ' ' + p
            
           
       
            names.append({'label':name , 'value':company.id, 'descr':company.last_name, 'img':name})
            
            
        # for company in qsc:
        #     names.append({'label':company.descripcion, 'value':company.user_id})
        

        return HttpResponse(json.dumps(names), content_type='application/json')
    
    
    
def search_auto(request):
    if request.is_ajax():    
        q = request.GET.get('term', '')
        uname = CustomUser.objects.filter(first_name__istartswith = q)    
        results = []
        for u in uname:
            user_json = {'value':0, 'image':0, 'label':0}
            user_json['value'] = u.id
            user_json['label'] = u.first_name
            user_json['img'] = u.picture               
            results.append(user_json)
        
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

        # return JsonResponse(names,safe = False)
    # return render(request, 'profile/profile-user-edit.html')


    # def __str__(self):
    #     return 'Comment by {} on {}'.format(self.name, self.post)


# <a href="{{ context.document.url}}" class="btn btn-primary" target="_blank"> Download SLides</a>
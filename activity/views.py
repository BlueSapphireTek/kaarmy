from django.shortcuts import render

# Create your views here.
from social.models import Post,Like

from byhand.models import Bio
from longprofile.models import CreateEvent,SavedEvent,CreateEnquiry,SavedEnquiry,CreateAppoinment2

import datetime as dt
from datetime import datetime
import datetime


def activitypost(request):
    try:
        bioview = Bio.objects.get(user_id = request.user.id)
    except:
        bioview = ""
    company = request.user.groups.filter(name='COMPANY').exists()
    postcount = Post.objects.filter(user_id=request.user.id).count()
    post_items = Post.objects.filter(user_id = request.user.id,privacy = 1,is_deleted = 0)
    eventcount = CreateEvent.objects.filter(user_id = request.user.id).count()
    enquirycount = CreateEnquiry.objects.filter(enquired_person_id=request.user.id).count()
    myevents = CreateEvent.objects.filter(user_id=request.user.id)
    liked_posts = [i for i in post_items if Like.objects.filter(post_id=i, user_id=request.user.id)]

    
    context = {
        'post_items':post_items,
        'postcount':postcount,
        'bioview':bioview,
        'liked_posts':liked_posts,
        'eventcount':eventcount,
        'enquirycount':enquirycount,
        'company':company
    }
    return render(request,'activities/activity-post.html',context)

def activitypostalluser(request,pk):
    company = request.user.groups.filter(name='COMPANY').exists()
    try:
        bioview = Bio.objects.get(user_id = request.user.id)
    except:
        bioview = ""

    postcount = Post.objects.filter(user_id=pk).count()
    post_items = Post.objects.filter(user_id = pk,privacy = 1,is_deleted = 0)
    eventcount = CreateEvent.objects.filter(user_id = pk).count()
    enquirycount = CreateEnquiry.objects.filter(enquired_person_id=pk).count()
    myevents = CreateEvent.objects.filter(user_id=request.user.id)
    liked_posts = [i for i in post_items if Like.objects.filter(post_id=i, user_id=request.user.id)]

   
    context = {
        'post_items':post_items,
        'postcount':postcount,
        'bioview':bioview,
        'liked_posts':liked_posts,
        'eventcount':eventcount,
        'enquirycount':enquirycount,
        'company':company,
        'otheruser':pk
    }
    return render(request,'activities/activity-post-alluser.html',context)


def event(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    postcount = Post.objects.filter(user_id=request.user.id).count()
    bios = Bio.objects.all()
    myevents = CreateEvent.objects.filter(user_id = request.user.id)
    eventcount = CreateEvent.objects.filter(user_id = request.user.id).count()
    enquirycount = CreateEnquiry.objects.filter(enquired_person_id=request.user.id).count()
    savedevents = SavedEvent.objects.filter(savedperson_id = request.user.id)

    #liked_posts = [i for i in post_items if Like.objects.filter(post_id=i, user_id=request.user.id)]
    # profile = [i for i in myevents if Bio.objects.filter()]
    

    context = {
        'myevents':myevents,
        'savedevents':savedevents,
        'bios':bios,
        'postcount':postcount,
        'eventcount':eventcount,
        'enquirycount':enquirycount,
        'company':company
    }
    return render(request,'activities/activity-event-main.html',context)

def enquiry(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    postcount = Post.objects.filter(user_id=request.user.id).count()
    eventcount = CreateEvent.objects.filter(user_id=request.user.id).count()
    enquiries = CreateEnquiry.objects.filter(enquired_person_id = request.user.id)
    enquirycount = CreateEnquiry.objects.filter(enquired_person_id = request.user.id).count()
    myenquiries = CreateEnquiry.objects.filter(user_id = request.user.id)
    savedenquiry = SavedEnquiry.objects.filter(savedperson_id = request.user.id)
    savedenquiries = [i for i in enquiries if SavedEnquiry.objects.filter(savedperson_id=request.user.id, enquiry_id=i)]
    context = {
        'enquiries':enquiries,
        'myenquiries':myenquiries,
        'savedenquiry':savedenquiry,
        'savedenquiries':savedenquiries,
        'postcount':postcount,
        'enquirycount':enquirycount,
        'eventcount':eventcount,
        'company':company

    }
    return render(request,'activities/activity-enquiry.html',context)

def appointment(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    postcount = Post.objects.filter(user_id=request.user.id).count()
    eventcount = CreateEvent.objects.filter(user_id=request.user.id).count()
    enquirycount = CreateEnquiry.objects.filter(enquired_person_id=request.user.id).count()
    date = datetime.datetime.now()

    pending = CreateAppoinment2.objects.filter(dateandtime__gte = date,active = 0,enquired_person_id = request.user.id)
    actived = CreateAppoinment2.objects.filter(dateandtime__gte=date, active=1, enquired_person_id= request.user.id)
    complete = CreateAppoinment2.objects.filter(dateandtime__lte=date, enquired_person_id= request.user.id)


    requestedpending = CreateAppoinment2.objects.filter(dateandtime__gte = date,active = 0,user_id=request.user.id)
    requestedactived = CreateAppoinment2.objects.filter(dateandtime__gte=date, active=1,user_id=request.user.id)
    requestedcomplete= CreateAppoinment2.objects.filter(dateandtime__lte=date,user_id=request.user.id)

  

    context = {
        'pending':pending,
        'actived':actived,
        'complete':complete,
        'requestedpending':requestedpending,
        'requestedactived':requestedactived,
        'requestedcomplete':requestedcomplete,
        'postcount':postcount,
        'eventcount':eventcount,
        'enquirycount':enquirycount,
        'company':company

    }
    return render(request,'activities/activity-appointment.html',context)

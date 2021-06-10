from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import *
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Prefetch
from django.db.models import Q
from longprofile.models import *


# Create your views here.
@login_required(login_url='login')
def chatroom(request,pk:int):
    current_user = request.user.id
    other_user = get_object_or_404(CustomUser, pk=pk)
    messages = Message.objects.filter(Q(receiver=request.user, sender=other_user,receiver_delete=False))
    messages.update(seen=True)
    messages = messages | Message.objects.filter(Q(receiver=other_user, sender=request.user,sender_delete=False) )
    connected1 = Connection.objects.filter(connected_person_id = request.user.id, connection=1).values_list('user_id')
    connected2 = Connection.objects.filter(user_id = request.user.id, connection=1).values_list('connected_person_id')
    connecteduser1 = CustomUser.objects.filter(id__in = connected1)
    connecteduser2 = CustomUser.objects.filter(id__in = connected2)
    connecteduser = connecteduser1 | connecteduser2
    currentuser = Bio.objects.get(user_id=request.user.id)
    currentuserimg = currentuser.image
    context = {
        "other_user": other_user,
        "messages": messages,
        "current_user":current_user,
        "connecteduser":connecteduser,
        "currentuserimg":currentuserimg
    }
    return render(request, "chat/onetoonechat.html",context)
@login_required(login_url='login')
def chatroom_base(request):
    connected1 = Connection.objects.filter(connected_person_id = request.user.id, connection=1).values_list('user_id')
    connected2 = Connection.objects.filter(user_id = request.user.id, connection=1).values_list('connected_person_id')
    connecteduser1 = CustomUser.objects.filter(id__in = connected1)
    connecteduser2 = CustomUser.objects.filter(id__in = connected2)
    connecteduser = connecteduser1 | connecteduser2
    currentuser = Bio.objects.get(user_id=request.user.id)
    currentuserimg = currentuser.image
    context = {
        "connecteduser":connecteduser,
        "currentuserimg":currentuserimg,
    }
    return render(request, "chat/onetoonechat_base.html",context)
@login_required(login_url='login')
def ajax_load_messages(request,pk):
    message_list = []
    other_user = get_object_or_404(CustomUser, pk=pk)
    messages = Message.objects.filter(seen=False).filter(Q(receiver=request.user, sender=other_user))
    for message in messages:
        if message.files == '':
            message_list = [{
                "id":message.id,
                "sender": message.sender.id,
                "message": message.message,
                "sent": message.sender == request.user,
                "file": ''
                
            } ]
        else:
            message_list = [{
                "id":message.id,
                "sender": message.sender.id,
                "message": message.message,
                "sent": message.sender == request.user,
                "file":message.files.url
            } ]
        messages.update(seen=True)
    if request.method == "POST":
        a = request.POST.get('message')
        b = request.FILES.get('upload')
        if a == '' and b == None:
            message_list.append({
                    "id":'',
                    "sender": '',
                    "message": '',
                    "sent": '',
                    "file":''
                })
        else:
            m = Message.objects.create(receiver=other_user, sender=request.user, message=a, files=b)
            if m.files == None:
                message_list.append({
                    "id":m.id,
                    "sender": request.user.id,
                    "message": m.message,
                    "sent": True,
                    "file":''
                })
            else:
                message_list.append({
                    "id":m.id,
                    "sender": request.user.id,
                    "message": m.message,
                    "sent": True,
                    "file":m.files.url
                })
    return JsonResponse(message_list, safe=False)
@login_required(login_url='login')
def messageDelete(request):
    a = request.POST.get('id')
    d = Message.objects.get(pk=a)
    if d.receiver_id == request.user.id:
        d.receiver_delete=True
        d.save()
    elif d.sender_id == request.user.id:
        d.sender_delete=True
        d.save()
    else:
        pass
    return HttpResponse('')
# @login_required
# def switchUser(request):
#     current_user = request.user
#     connecteduser = CustomUser.objects.all()
#     last_seen = cache.get('seen_%s' % connecteduser)
#     return HttpResponse('')
# Group chat.
@login_required(login_url='login')
def createGroup(request):
    if request.method == "POST":
        group = Group()
        group.name = request.POST.get('groupname')
        group.icon = request.FILES.get('groupicon')
        group.save()
        c = request.POST.get('members')
        arr = c.split(',')
        for i in arr:
            groupmembers = GroupMembers()
            groupmembers.group = group
            d = int(i)
            groupmembers.member_id = d
            groupmembers.admin = False
            groupmembers.save()
        groupmembers = GroupMembers()
        groupmembers.group = group
        groupmembers.member_id = request.user.id
        groupmembers.admin = True
        groupmembers.save()
        
    return HttpResponse('')
@login_required(login_url='login')
def groupchatroom(request,pk:int):
    current_user = request.user.id
    messages = GroupMessage.objects.filter(group_id = pk)
     
    for i in messages:
            mes = GroupSeen.objects.get(message_id = i.id, member_id = request.user.id)
            mes.seen = True
            mes.save()
    connected1 = Connection.objects.filter(connected_person_id = request.user.id, connection=1).values_list('user_id')
    connected2 = Connection.objects.filter(user_id = request.user.id, connection=1).values_list('connected_person_id')
    connecteduser1 = CustomUser.objects.filter(id__in = connected1)
    connecteduser2 = CustomUser.objects.filter(id__in = connected2)
    connecteduser = connecteduser1 | connecteduser2
    #update user
    members_in_grp =GroupMembers.objects.filter(group_id=pk).values_list('member_id')
    updatelist = CustomUser.objects.filter(~Q(id__in = members_in_grp))

    members =GroupMembers.objects.filter(member_id=request.user.id).values_list('group_id')
    group = Group.objects.filter(id__in = members)
    current_group = Group.objects.get(pk = pk)
    group_id = pk
    currentuser = Bio.objects.get(user_id=request.user.id)
    currentuserimg = currentuser.image
    context = {
        "messages": messages,
        "connecteduser":connecteduser,
        "group":group,
        "group_id":group_id,
        "current_group":current_group,
        "updatelist":updatelist,
        "currentuserimg":currentuserimg
    }
    return render(request, "chat/groupchat.html",context)
@login_required(login_url='login')
def groupchatroom_base(request):
    connected1 = Connection.objects.filter(connected_person_id = request.user.id, connection=1).values_list('user_id')
    connected2 = Connection.objects.filter(user_id = request.user.id, connection=1).values_list('connected_person_id')
    connecteduser1 = CustomUser.objects.filter(id__in = connected1)
    connecteduser2 = CustomUser.objects.filter(id__in = connected2)
    connecteduser = connecteduser1 | connecteduser2
    members =GroupMembers.objects.filter(member_id=request.user.id).values_list('group_id')
    group = Group.objects.filter(id__in = members)
    currentuser = Bio.objects.get(user_id=request.user.id)
    currentuserimg = currentuser.image
    context = {
        "connecteduser":connecteduser,
        "group":group,
        "currentuserimg":currentuserimg,
    }
    return render(request, "chat/groupchatbase.html",context)    
@login_required(login_url='login')
def ajax_load_messages_group(request,pk):
    message_list = []
    a = ''
    group_id = pk
    # messages = Message.objects.filter(seen=False).filter(Q(receiver=request.user, sender=other_user))
    # messages = GroupMessage.objects.filter(seen=False).filter(group_id = pk)
    messages1 = GroupMessage.objects.filter(group_id = pk)
    for i in messages1:
        try:
            mes = GroupSeen.objects.get(message_id = i.id, member_id = request.user.id, seen = False)
            a = str(mes.message_id)
        except:
            a = ''
    if len(a)>0:
        b =int(a)
        messages = GroupMessage.objects.filter(id = a)
        for message in messages:
            if message.files == '':
                message_list = [{
                    "sender": message.member_id,
                    "message": message.chat,
                    "sent": message.member_id == request.user,
                    "file": '',
                    "mName":message.member.first_name
                    
                } ]
            else:
                message_list = [{
                    "sender": message.member_id,
                    "message": message.chat,
                    "sent": message.member_id == request.user,
                    "file":message.files.url,
                    "mName":message.member.first_name
                } ]
            groupseen = GroupSeen.objects.get(message_id = b, member_id = request.user.id)
            groupseen.seen = True
            groupseen.save()
    if request.method == "POST":
        a = request.POST.get('message')
        b = request.FILES.get('upload')
        if a == '' and b == None:
            message_list.append({
                    "sender": '',
                    "message": '',
                    "sent": '',
                    "file":'',
                    "mName":''
                })
        else:
            m = GroupMessage.objects.create(group_id=group_id, member_id=request.user.id, chat=a, files=b)
            if m.files == None:
                message_list.append({
                    "sender": request.user.id,
                    "message": m.chat,
                    "sent": True,
                    "file":'',
                    "mName":m.member.first_name
                })
            else:
                message_list.append({
                    "sender": request.user.id,
                    "message": m.chat,
                    "sent": True,
                    "file":m.files.url,
                    "mName":m.member.first_name
                })
            members = GroupMembers.objects.filter(group_id=group_id)
            for i in members:
                groupseen = GroupSeen()
                groupseen.member_id = i.member_id
                groupseen.message_id = m.id
                groupseen.group_id = pk
                if i.member_id == request.user.id:
                    groupseen.seen = True
                else:
                    groupseen.seen = False
                groupseen.save()
    return JsonResponse(message_list, safe=False)
@login_required(login_url='login')
def messageDelete_group(request):
    a = request.POST.get('id')
    d = Message.objects.get(pk=a)
    # d.delete()
    return HttpResponse('')
@login_required(login_url='login')
def updateGroupinfo(request,pk):
    update = Group.objects.get(pk=pk)
    if request.POST.get('groupname') != "":
        update.name = request.POST.get('groupname')
    if request.FILES.get('groupicon') != None:
        update.icon = request.FILES.get('groupicon')
    update.save()
    return HttpResponse('')
@login_required(login_url='login')
def updateGroupMembers(request,pk):
    c = request.POST.get('members')
    arr = c.split(',')
    for i in arr:
        groupmembers = GroupMembers()
        groupmembers.group_id = pk
        d = int(i)
        groupmembers.member_id = d
        groupmembers.admin = False
        groupmembers.save()
        groupseen = GroupSeen.objects.filter(group_id=pk,member_id=request.user.id)
        for j in groupseen:
            groupseen1 = GroupSeen()
            groupseen1.message_id = j.message_id
            groupseen1.member_id = d
            groupseen1.group_id = pk
            groupseen1.seen = True
            groupseen1.save()
    return HttpResponse('')
@login_required(login_url='login')
def exitgroup(request,pk):
    exit = GroupMembers.objects.get(group_id=pk, member_id=request.user.id)
    exit.delete()
    return HttpResponse('')
@login_required(login_url='login')
def chatcount(request):
    onetoonechat = 0
    current_user = request.user.id
    onetoonechat = Message.objects.filter(receiver_id = current_user,seen=False).count()
    return {'onetoonechat': onetoonechat}
     
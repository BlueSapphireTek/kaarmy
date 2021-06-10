from django.shortcuts import render
import string,random

# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login ,update_session_auth_hash,logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse ,HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from byhand.models import CustomUser

from byhand.models import UserExtend
from social.models import Notification
from django.views.decorators.csrf import csrf_exempt

from byhand.models import Follow,Bio
from django.contrib.auth.models import Group
from django.db.models import Q
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage



@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    
    digits = ''.join(random.sample(string.digits, 6))
    chars = ''.join(random.sample(string.ascii_lowercase, 6))
    
    uname = digits+chars
    user.username = uname
    
    user.is_active = True
    
    user.save()

def regcheck(request):
    try:
        
        u = UserExtend.objects.get(user_id = request.user.id)
        
        return redirect('timeline')
    except:
        return redirect('register_as')
        
        

def register(request):
    Email = request.POST.get('email')
    Username = request.POST.get('phoneno')
    Password = request.POST.get('password1')
    #password = make_password(Password)
    digits = ''.join(random.sample(string.digits, 6))
    chars = ''.join(random.sample(string.ascii_lowercase, 6))
    uname = digits+chars
    
    if request.method == "POST":
        user = CustomUser()
        user.email = Email
        user.phone = Username
        user.username = uname
        user.set_password(Password)
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request,user)
        return redirect('register_as')
    return render(request,'registration/registration-byhand.html')

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get('email')
    

    user_obj = CustomUser.objects.filter(email = email).exists()
    print(user_obj)
    
    
   
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_phone_exist(request):
    phone = request.POST.get('phoneno')
    user_obj = CustomUser.objects.filter(phone = phone).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_email_existe(request):
    email = request.POST.get('email')
    

    user_obj = CustomUser.objects.filter(email = email).exclude(id= request.user.id).exists()
    print(user_obj)
    
    
   
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_phone_existe(request):
    phone = request.POST.get('phoneno')
    user_obj = CustomUser.objects.filter(phone = phone).exclude(id= request.user.id).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def dashboard(request):
    return render(request,'dashboard.html')
def loginpage(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')


        # user = authenticate(request, email=username, password=password)
        try:
            user = CustomUser.objects.get(phone = username)

            if user.check_password(password):

                
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
                
                return redirect('timeline')


        except CustomUser.DoesNotExist:
            messages.error(request, 'invalid credentials')
            try:
                user = CustomUser.objects.get(email=username)
                if user.check_password(password):
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request,user)
                    return redirect('timeline')


            except:

                messages.error(request, 'username or password is incorrect')
                # return redirect('dashboard')







        # if user is not None:
        #
        #
        #     login(request, user)
        #     return redirect('dashboard')
        # else:
        #     messages.info(request, 'None user')



    return render(request,'registration/byhand-login.html')



def register_as(request):
    return render(request,'registration/registration-as.html')
def register_company(request):
    view = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        Company = request.POST.get('cname')
        Createdby = request.POST.get('createdby')
        Position = request.POST.get('position')
        Email = request.POST.get('email')
        Mobile = request.POST.get('phone')
        view.email= Email
        view.phone = Mobile
        view.first_name = Company
        view.save()
        userextend = UserExtend()
        userextend.company_name = Company
        userextend.created_by = Createdby
        userextend.position = Position
        userextend.user_id = request.user.id
        userextend.group = 'Company'

        userextend.save()
        
        bio = Bio()
        bio.user_id = request.user.id
        bio.save()
        

        my_doctor_group = Group.objects.get_or_create(name='COMPANY')
        my_doctor_group[0].user_set.add(request.user)
        return redirect('companyprofile')


    context = {
        'view': view
    }
    return render(request,'registration/registration-company.html',context)
def register_freelancer(request):
    view = CustomUser.objects.get(id= request.user.id)


    if request.method == "POST":

        First_Name = request.POST.get('first_name')
        Last_Name = request.POST.get('last_name')
        Email = request.POST.get('email')
        Mobile = request.POST.get('phone')
        Profession = request.POST.get('profession')
        view.first_name = First_Name
        view.last_name = Last_Name
        view.email = Email
        view.phone = Mobile
        view.save()
        userextend = UserExtend()
        userextend.profession = Profession
        userextend.user_id = request.user.id
        userextend.group = 'Freelancer'
        userextend.save()

        bio = Bio()
        bio.user_id = request.user.id
        bio.save()

        my_doctor_group = Group.objects.get_or_create(name='FREELANCER')
        my_doctor_group[0].user_set.add(request.user)
        return redirect('userprofile')


    context = {
        'view': view
    }
    return render(request,'registration/registration-freelancer.html',context)

def register_professional(request):
    view = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":

        First_Name = request.POST.get('first_name')
        Last_Name = request.POST.get('last_name')
        Email = request.POST.get('email')
        Mobile = request.POST.get('phone')
        Profession = request.POST.get('profession')
        view.first_name = First_Name
        view.last_name = Last_Name
        view.email = Email
        view.phone = Mobile
        view.save()
        userextend = UserExtend()
        userextend.profession = Profession
        userextend.user_id = request.user.id
        userextend.group = 'Professional'
        userextend.save()
        
        bio = Bio()
        bio.user_id = request.user.id
        bio.save()

        my_doctor_group = Group.objects.get_or_create(name='PROFESSIONAL')
        my_doctor_group[0].user_set.add(request.user)

        return redirect('userprofile')

    context = {
        'view': view
    }


    return render(request,'registration/registration-professional.html',context)


def register_enterprenur(request):
    view = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":

        First_Name = request.POST.get('first_name')
        Last_Name = request.POST.get('last_name')
        Email = request.POST.get('email')
        Mobile = request.POST.get('phone')
        Profession = request.POST.get('profession')
        view.first_name = First_Name
        view.last_name = Last_Name
        view.email = Email
        view.phone = Mobile
        view.save()
        userextend = UserExtend()
        userextend.profession = Profession
        userextend.user_id = request.user.id
        userextend.group = 'Professional'
        userextend.save()
        
        bio = Bio()
        bio.user_id = request.user.id
        bio.save()

        my_doctor_group = Group.objects.get_or_create(name='ENTERPRENUR')
        my_doctor_group[0].user_set.add(request.user)

        return redirect('userprofile')

    context = {
        'view': view
    }


    return render(request,'registration/registration-enterprenur.html',context)

def register_public(request):
    view = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        First_Name = request.POST.get('first_name')
        Last_Name = request.POST.get('last_name')
        Email = request.POST.get('email')
        Mobile = request.POST.get('phone')



        view.first_name = First_Name
        view.last_name = Last_Name
        view.email = Email
        view.phone = Mobile
        view.save()

        userextend = UserExtend()
        userextend.user_id = request.user.id
        userextend.group = 'Public'
        userextend.save()

        bio = Bio()
        bio.user_id = request.user.id
        bio.save()

        


        my_doctor_group = Group.objects.get_or_create(name='PUBLIC')
        my_doctor_group[0].user_set.add(request.user)

        return redirect('userprofile')



    context = {
        'view': view
    }

    return render(request,'registration/registration-public.html',context)

def register_student(request):
    view = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        First_Name = request.POST.get('first_name')
        Last_Name = request.POST.get('last_name')
        Email = request.POST.get('email')
        Mobile = request.POST.get('phone')
        Degree = request.POST.get('degree')
        Specilization = request.POST.get('specialization')
        Startyear = request.POST.get('start_year')
        Endyear = request.POST.get('end_year')
        school = request.POST.get('school')
        view.first_name = First_Name
        view.last_name = Last_Name
        view.email = Email
        view.phone = Mobile
        view.save()
        userextend = UserExtend()
        userextend.degree = Degree

        userextend.start_year = Startyear
        userextend.end_year = Endyear
        userextend.institution_name = school
        userextend.specilisation = Specilization


        userextend.user_id = request.user.id
        userextend.group = 'Student'
        userextend.save()

        bio = Bio()
        bio.user_id = request.user.id
        bio.save()

    

        my_doctor_group = Group.objects.get_or_create(name='STUDENT')
        my_doctor_group[0].user_set.add(request.user)
        return redirect('userprofile')

    context = {
        'view': view
    }
    return render(request,'registration/registration-student.html',context)



###################################
def userslist(request):
    users = CustomUser.objects.all()

    context = {
        'users':users
    }
    return render(request,'userslist.html',context)

def userview(request,id):

    user = CustomUser.objects.get(id = id)
    followerscount = Follow.objects.filter(following_id = id)
    followers = followerscount.count()
    
    followingcount = Follow.objects.filter(follower_id = id)
    following = followingcount.count()
    
    followstatus = Follow.objects.filter(follower_id = request.user.id,following_id = id).exists()

    

   
    context = {
        'user': user,
        'followstatus': followstatus,
        'followers': followers,
        'following':following,
    }
    return render(request,'userview.html',context)

def follow(request,id):


    foll = Follow()
    foll.follower_id=request.user.id
    foll.following_id = id

    foll.save()

    return HttpResponse("true")



def unfollow(request,id):
    ufollow = Follow.objects.filter(follower_id = request.user.id,following_id = id)
    ufollow.delete()
    return HttpResponse("true")


############settings###############

def passwordchange_internal(request):
    currentuser = request.user.id
    company = currentuser.groups.filter(name='COMPANY').exists()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            return redirect('login')
        else:
            messages.error(request, '')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form':form
    }
    return render(request,'passwordchange/changepassword_internal.html',context)

def edit_profile(request):
    company = currentuser.groups.filter(name='COMPANY').exists()
    currentuser = request.user
    company = currentuser.groups.filter(name='COMPANY').exists()
    freelancer = currentuser.groups.filter(name='FREELANCER').exists()
    professional = currentuser.groups.filter(name='PROFESSIONAL').exists()
    public = currentuser.groups.filter(name='PUBLIC').exists()
    student = currentuser.groups.filter(name='STUDENT').exists()
    try:
        
        bioview = Bio.objects.get(user_id = request.user.id)
        if request.method == "POST":
            Name = request.POST.get('name')
            Lname = request.POST.get('lastname')
            Address = request.POST.get('address')
            Website = request.POST.get('website')
            Phonenumber = request.POST.get('phoneno')
            Email = request.POST.get('email')
            Gender = request.POST.get('gender')
            
            
            
            
            

            bioview.address = Address
            bioview.website = Website
            bioview.user_id = request.user.id
            bioview.gender = Gender
            bioview.save()

            cuser = CustomUser.objects.get(id= request.user.id)
            cuser.first_name = Name
            if Lname:
                cuser.last_name = Lname
            cuser.phone = Phonenumber
            cuser.email = Email
            cuser.save()
            return redirect('editprofile')

        context = {

            'bioview': bioview,
            'company': company,
        }

        return render(request, 'profile/edit_profile.html',context)

    except:
        
        bioview = None
        if request.method == "POST":
            company = currentuser.groups.filter(name='COMPANY').exists()
            freelancer = currentuser.groups.filter(name='FREELANCER').exists()
            professional = currentuser.groups.filter(name='PROFESSIONAL').exists()
            public = currentuser.groups.filter(name='PUBLIC').exists()
            student = currentuser.groups.filter(name='STUDENT').exists()
            Name= request.POST.get('name')
            Lname = request.POST.get('lastname')
            Address= request.POST.get('address')
            Website= request.POST.get('website')
            Phonenumber= request.POST.get('phoneno')
            Email= request.POST.get('email')
            Gender = request.POST.get('gender')
            

            bio = Bio()
            bio.address = Address
            bio.website = Website
            bio.user_id= request.user.id
            bio.gender = Gender
            bio.save()

            cuser = CustomUser.objects.get(id= request.user.id)
            cuser.first_name = Name
            if Lname:
                cuser.last_name = Lname
            cuser.phone = Phonenumber
            cuser.email = Email
            cuser.save()
            return redirect('editprofile')

        context = {

            'bioview': bioview,
            'company':company,
        }


        return render(request,'profile/edit_profile.html',context)


def editprofile(request):
    currentuser = request.user
    company = currentuser.groups.filter(name='COMPANY').exists()
    freelancer = currentuser.groups.filter(name='FREELANCER').exists()
    professional = currentuser.groups.filter(name='PROFESSIONAL').exists()
    public = currentuser.groups.filter(name='PUBLIC').exists()
    student = currentuser.groups.filter(name='STUDENT').exists()
    try:

        bioview = Bio.objects.get(user_id=request.user.id)
        if request.method == "POST":
            Name = request.POST.get('name')
            Lname = request.POST.get('lastname')
            Address = request.POST.get('address')
            Website = request.POST.get('website')
            Phonenumber = request.POST.get('phoneno')
            Email = request.POST.get('email')
            Gender = request.POST.get('gender')
            print(Gender)
            
            

            bioview.address = Address
            bioview.website = Website
            bioview.user_id = request.user.id
            bioview.gender = Gender
            bioview.save()

            cuser = CustomUser.objects.get(id=request.user.id)
            cuser.first_name = Name
            if Lname:
                cuser.last_name = Lname
            cuser.phone = Phonenumber
            cuser.email = Email
            cuser.save()
            return redirect('editprofile')

        context = {

            'bioview': bioview,
            'company': company,
        }

        return render(request,'settings/edit_profile.html',context)
    except:

        bioview = None
        if request.method == "POST":
            company = currentuser.groups.filter(name='COMPANY').exists()
            freelancer = currentuser.groups.filter(name='FREELANCER').exists()
            professional = currentuser.groups.filter(name='PROFESSIONAL').exists()
            public = currentuser.groups.filter(name='PUBLIC').exists()
            student = currentuser.groups.filter(name='STUDENT').exists()
            Name= request.POST.get('name')
            Lname = request.POST.get('lastname')
            Address= request.POST.get('address')
            Website= request.POST.get('website')
            Phonenumber= request.POST.get('phoneno')
            Email= request.POST.get('email')
            Gender = request.POST.get('gender')
            print(Gender)
            
            bio = Bio()
            bio.address = Address
            bio.website = Website
            bio.user_id= request.user.id
            bio.gender = Gender
            bio.save()

            cuser = CustomUser.objects.get(id= request.user.id)
            cuser.first_name = Name
            if Lname:
                cuser.last_name = Lname
            cuser.phone = Phonenumber
            cuser.email = Email
            cuser.save()
            if company:
                return redirect('companyprofile')
                
            else:
                return redirect('userprofile')
            
            
            # return redirect('editprofile')

        context = {

            'bioview': bioview,
            'company':company,
        }

        return render(request, 'settings/edit_profile.html',context)


def changeprofile(request):
    try:
        bio = Bio.objects.get(user_id = request.user.id)
        if request.method == "POST":
            Image = request.FILES.get('file')
            
            bio.image = Image
            bio.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        # bioview = None
        if request.method == "POST":
            Image = request.FILES.get('file')
            bio = Bio()
            bio.image = Image
            bio.user_id = request.user.id
            bio.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def change_password(request):
    try:
        bioview = Bio.objects.get(user_id=request.user.id)
    except:
        bioview = None
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            messages.success(request, "Success: Password Reset Sucessfully")
        else:
            
            # messages.success(request, "Success: This is the sample success Flash message.")
            messages.error(request, "Error: Old Password Is Incorrect")
            # messages.info(request, "Info: This is the sample info Flash message.")
            # messages.warning(request, "Warning: This is the sample warning Flash message.")
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'bioview':bioview,
        'form':form,
    }
    return render(request,'settings/change_password.html',context)


#########################forgot password #######################333

def reset_password(request):
    if request.method == 'POST':
        Email = request.POST.get('email')
        try:

            user = CustomUser.objects.get(email = Email)

        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None


        if user is not None:
            current_site = get_current_site(request)
            mail_subject = 'Reset Password link'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = Email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            
            return redirect('password_reset_done')
        else:
            messages.info(request, 'invalid email')


    return render(request,"passwordchange/password_reset.html")

@csrf_exempt
def reseta(req, uidb64 ,token):

    d=9
    

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
       
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None



            #form = PasswordChangingForm()#

    if user is not None and req.method == 'POST':

        a=1
        

        Password = req.POST.get('new_password1')
        Password2 = req.POST.get('new_password2')

        userp = CustomUser.objects.get(pk=uid)
        

        
        password = make_password(Password)
        
        userp.set_password(Password)
        userp.is_active = True
                                             #form = PasswordChangingForm(req.POST)#


        userp.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(req,user)

        


        return redirect('password_reset_complete')
    return render(req,'passwordchange/password_reset_form.html')

def showNotification(request):
    company = request.user.groups.filter(name='COMPANY').exists()
    notifications = Notification.objects.filter(user_id = request.user.id).order_by('-date')
    Notification.objects.filter(user_id =request.user.id, is_seen=False).update(is_seen=True)
    
    try:
        bioview = Bio.objects.get(user = request.user.id)
    except:
        bioview = None

    context = {
        'notifications': notifications,
        'bioview':bioview,
        'company':company,
    }
    return render(request,'timeline/notifications.html',context)

def CountNotifications(request):
    count_notifications = None
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(~Q(notification_type=3) ,user_id =request.user.id, is_seen=False ).count()
    return {'count_notifications': count_notifications}


def certificate_notification(request):
    notifications = Notification.objects.filter(user_id=request.user.id ,notification_type = 3).order_by('-date')
    Notification.objects.filter(user_id=request.user.id, is_seen=False,notification_type = 3).update(is_seen=True)

    try:
        bioview = Bio.objects.get(user = request.user.id)
    except:
        bioview = None

    context = {
        'notifications':notifications,
        'bioview':bioview,
    }
    return render(request, 'timeline/certificate_notifications.html', context)

def logoutuser(request):

	logout(request)
	return redirect('login')

def Certificate_CountNotifications(request):
    cer_count_notifications = None
    if request.user.is_authenticated:
        cer_count_notifications = Notification.objects.filter(user_id =request.user.id, is_seen=False,notification_type = 3).count()
    return {'cer_count_notifications': cer_count_notifications}










"""byhandpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from byhand import views
from django.views.static import serve
from byhandpro import settings
from django.contrib.auth import views as auth_views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
handler404 = 'longprofile.views.not_found'
handler500 = 'longprofile.views.server_error'


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('register/', views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.loginpage,name='login'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('accounts/',include('allauth.urls')),
    path('regcheck/',views.regcheck,name='regcheck'),


    #######
    path('check_email_exist/',views.check_email_exist,name='check_email_exist'),
    path('check_phone_exist/',views.check_phone_exist,name='check_phone_exist'),
    
    path('check_email_existe/',views.check_email_existe,name='check_email_existe'),
    path('check_phone_existe/',views.check_phone_existe,name='check_phone_existe'),
    #######

    path('register_as/',views.register_as,name='register_as'),
    path('register_company/',views.register_company,name='register_company'),
    path('register_freelancer/',views.register_freelancer,name='register_freelancer'),
    path('register_professional/',views.register_professional,name='register_professional'),
    path('register_public/',views.register_public,name='register_public'),
    path('register_student/',views.register_student,name='register_student'),
    path('register_enterprenur/',views.register_enterprenur,name='register_enterprenur'),
    ###########
    path('userslist/',views.userslist,name='userslist'),
    path('userview/<int:id>/',views.userview,name='userview'),
    path('follow/<int:id>/',views.follow,name='follow'),
    path('unfollow/<int:id>/',views.unfollow,name='unfollow'),

    ##############settings#################
    path('change_password_internal/',views.passwordchange_internal,name = 'change_password_internal'),
    path('edit_profile/',views.edit_profile,name = 'edit_profile'),
    path('changeprofile/',views.changeprofile,name = 'changeprofile'),
    path('change_password/',views.change_password,name ='change_password'),
    
    
    ###################forgot password#####################
    # path('resetpassword/',views.resetpassword,name ='resetpassword'),
    # path('reset_password/',
    #     auth_views.PasswordResetView.as_view(template_name="passwordchange/password_reset.html"),
    #     name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="passwordchange/password_reset_sent.html"),
         name="password_reset_done"),
    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name="passwordchange/password_reset_form.html"),
    #      name="password_reset_confirm"),
    
    # path('password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='users/password_reset_confirm.html'
    #      ),
    #      name='password_reset_confirm'),
    
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="passwordchange/password_reset_done.html"),
         name="password_reset_complete"),
    
    
    path('reset_passwordc/',views.reset_password,name ="reset_passwordc"),
    
    path('reseta/<uidb64>/<token>/',views.reseta, name='reseta'),    

    #############Settings ##############

    #####
    path('social/',include("social.urls")),

    ###################settings########################
    path('editprofile/',views.editprofile,name="editprofile"),
    #################notification#########################

    path('notification/',views.showNotification,name="notification"),
    path('certificate_notification/',views.certificate_notification,name="certificate_notification"),

    path('longprofile/',include("longprofile.urls")),
    path('chat/',include("chat.urls")),
    path('activity/',include("activity.urls")),

    # url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

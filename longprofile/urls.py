from django.conf.urls import url
from django.urls import path
from longprofile import views

urlpatterns = [
    path('home/',views.home,name="home"),
    path('cards/',views.cards,name="cards"),
    path('company_card_update/',views.company_card_update,name="company_card_update"),
    path('personal_card_update/',views.personal_card_update,name="personal_card_update"),
    url('^personalcardDelete/(?P<pk>\d+)/$',views.personalcardDelete,name="personalcardDelete"),
    url('^personalcardview/(?P<slug>[-\w]+)-(?P<pk>\d+)/$',views.personalcardview,name="personalcardview"),
    url('^personalcardviewpdf/(?P<pk>\d+)/$',views.personalcardviewpdf,name="personalcardviewpdf"),
    path('autosuggest', views.autosuggest, name='autosuggest'),
    path('manualsearch', views.manualsearch, name='manualsearch'),
    url(r'^searchprofile_full_view/(?P<pk>\d+)/$',views.searchprofile_full_view,name="searchprofile_full_view"),
    path('profile_full_view/',views.profile_full_view,name="profile_full_view"),
    path('home2/',views.home2,name="home2"),
    path('starRating/',views.starRating,name="starRating"),
    # path('follow/<str:username>',views.follow,name="follow"),
    url('^follow/(?P<pk>\d+)/$',views.follow,name="follow"),
    url('^countAndNotifications/(?P<pk>\d+)/$',views.countAndNotifications,name="countAndNotifications"),
    url('^endorse/(?P<pk>\d+)/$',views.endorse,name="endorse"),
    url('^connection/(?P<pk>\d+)/$',views.connection,name="connection"),
    url('^connectionList/(?P<pk>\d+)/$',views.connectionList,name="connectionList"),
    url('^connectionDelete/(?P<pk>\d+)/$',views.connectionDelete,name="connectionDelete"),
    url('^connectionAccept/(?P<pk>\d+)/$',views.connectionAccept,name="connectionAccept"),
    #event
    path('createevent/',views.createevent,name="createevent"),
    url('^eventOtheruser/(?P<pk>\d+)/$',views.eventOtheruser,name="eventOtheruser"),
    url('^eventSave/(?P<pk>\d+)/$',views.eventSave,name="eventSave"),
    url('^deleteevent/(?P<pk>\d+)/$',views.deleteevent,name="deleteevent"),
    #enquiry
    url('^createEnquiry/(?P<pk>\d+)/$',views.createEnquiry,name="createEnquiry"),
    url('^myenquiry/',views.myenquiry,name="myenquiry"),
    url('^enquirySave/(?P<pk>\d+)/$',views.enquirySave,name="enquirySave"),
    url('^deleteenquiry/(?P<pk>\d+)/$',views.deleteenquiry,name="deleteenquiry"),
    #appoinment
    url('^createAppoinment/(?P<pk>\d+)/$',views.createAppoinment,name="createAppoinment"),
    url('^myappoinment/',views.myappoinment,name="myappoinment"),
    url('^approveappointment/(?P<pk>\d+)/$',views.approveappointment,name="approveappointment"),
    url('^updateappointment/(?P<id>\d+)/$',views.updateappointment,name="updateappointment"),
    url('^deleteappointment/(?P<pk>\d+)/$',views.deleteappointment,name="deleteappointment"),
    #delete
    url('^expertisedelete/(?P<pk>\d+)/$',views.expertisedelete,name="expertisedelete"),
    url('^experiencedelete/(?P<pk>\d+)/$',views.experiencedelete,name="experiencedelete"),
    url('^projectsdelete/(?P<pk>\d+)/$',views.projectsdelete,name="projectsdelete"),
    url('^achievementsdelete/(?P<pk>\d+)/$',views.achievementsdelete,name="achievementsdelete"),
    url('^certificationdelete/(?P<pk>\d+)/$',views.certificationdelete,name="certificationdelete"),
    url('^clientdelete/(?P<pk>\d+)/$',views.clientdelete,name="clientdelete"),
    url('^testimonialdelete/(?P<pk>\d+)/$',views.testimonialdelete,name="testimonialdelete"),
    #about
    path('aboutupdate/',views.aboutupdate,name="aboutupdate"),
]
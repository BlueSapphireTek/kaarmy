from django.urls import path
from activity import views

urlpatterns = [
    path('activitypost/',views.activitypost,name="activitypost"),
    path('activitypostalluser/<int:pk>/',views.activitypostalluser,name="activitypostalluser"),
    path('event/',views.event,name="event"),
    path('enquiry/',views.enquiry,name="enquiry"),
    path('appointment/',views.appointment,name="appointment"),
]
from django.urls import path
from chat import views

urlpatterns = [
    path("chatroom/<int:pk>", views.chatroom, name = "chatroom"),
    path("ajax/<int:pk>/", views.ajax_load_messages, name="chatroom-ajax"),
    path("messageDelete/", views.messageDelete, name="messageDelete"),
    # path("switchUser/", views.switchUser, name="switchUser"),
    path("createGroup/", views.createGroup, name="createGroup"),
    path("groupchatroom/<int:pk>/", views.groupchatroom, name = "groupchatroom"),
    path("groupchatroom_base/", views.groupchatroom_base, name = "groupchatroom_base"),
    path("ajax_load_messages_group/<int:pk>/", views.ajax_load_messages_group, name="ajax_load_messages_group"),
    path("messageDelete_group/", views.messageDelete_group, name="messageDelete_group"),
    path("updateGroupinfo/<int:pk>/", views.updateGroupinfo, name="updateGroupinfo"),
    path("updateGroupMembers/<int:pk>/", views.updateGroupMembers, name="updateGroupMembers"),
    path("exitgroup/<int:pk>/", views.exitgroup, name="exitgroup"),
    path("chatroom_base/", views.chatroom_base, name="chatroom_base"),
    path("chatcount/", views.chatcount, name="chatcount"),
]
from django.conf.urls import url
from django.urls import path
from social import views

urlpatterns = [

    path('post/',views.PostView,name="post"),
    path('index/',views.index,name="index"),
    path('timeline/',views.timeline,name="timeline"),


    path('like/<int:id>',views.like,name="like"),
    path('dislike/<int:id>',views.dislike,name="dislike"),
    path('likecount/<int:id>',views.likecount,name="likecount"),
    path('postlike/<int:id>',views.postlike,name="postlike"),

    path('comment/',views.comment,name="comment"),
    path('postreport/',views.postreport,name="postreport"),
    path('postDelete/',views.postDelete,name="postDelete"),

    path('enquiry/',views.enquiry,name="enquiry"),

    path('post-detail/<int:id>',views.post_detail,name="post_detail"),

    path('profile/',views.profile,name="profile"),
    path('companyprofile/',views.companyprofile,name="companyprofile"),
    path('userprofile/',views.userprofile,name="userprofile"),


    path('companyprofileview/<int:id>/',views.companyprofileview,name="companyprofileview"),
    path('userprofileview/<int:id>/',views.userprofileview,name="userprofileview"),

    path('experience/',views.experience,name="experience"),
    path('editexperience/<int:id>',views.editexperience,name="editexperience"),


    path('experiencelist/<int:id>',views.experiencelist,name="experiencelist"),

    path('addworking/',views.addworking,name="addworking"),
    path('transalator/',views.transalator,name="transalator"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('achievements/',views.achievements,name="achievements"),
    path('addachievements/',views.addachievements,name="addachievements"),
    path('editachievements/<int:id>',views.editachievements,name="editachievements"),

    path('projects/',views.projects,name="projects"),
    path('editprojects/<int:id>',views.editprojects,name="editprojects"),

    path('cexpertise/',views.cexpertise,name="cexpertise"),
    path('expertise/',views.expertise,name="expertise"),
    path('editexpertise/<int:id>',views.editexpertise,name="editexpertise"),


    path('experience/',views.experience,name="experience"),

    path('addclient/',views.addclient,name="addclient"),
    path('editclient/<int:id>',views.editclient,name="editclient"),

    path('addtestimonial/',views.addtestimonial,name="addtestimonial"),
    path('edittestimonial/<int:id>',views.edittestimonial,name="edittestimonial"),

    path('addcertificate/',views.addcertificate,name="addcertificate"),
    path('editcertificate/<int:id>',views.editcertificate,name="editcertificate"),

    path('addbranch/',views.addbranch,name="addbranch"),
    path('editbranch/<int:id>',views.editbranch,name="editbranch"),

    path('addabout',views.addabout,name="addabout"),
    path('addlocation',views.addlocation,name="addlocation"),
    ##################sharepage#####################
    path('share/',views.share,name="share"),
    path('addbrousher',views.addbrousher,name="addbrousher"),
    path('addcard',views.addcard,name="addcard"),
    path('addimage',views.addimage,name="addimage"),
    path('adddocs',views.adddocs,name="adddocs"),

    ######################verification ###########################

    path('verifycertificate/',views.verifycertificate,name="verifycertificate"),
    path('approvecertificate/<int:id>',views.approvecertificate,name="approvecertificate"),
    path('deletecertificate/<int:id>',views.deletecertificate,name="deletecertificate"),
    path('editverificationcertificate/<int:id>',views.editverificationcertificate,name="editverificationcertificate"),
    path('sendvercertificate/<int:id>',views.sendvercertificate,name="sendvercertificate"),


    path('verifyclient/',views.verifyclient,name="verifyclient"),
    path('editverificationclient/<int:id>',views.editverificationclient,name="editverificationclient"),
    path('deleteclient/<int:id>',views.deleteclient,name="deleteclient"),
    path('approveclient/<int:id>',views.approveclient,name="approveclient"),
    path('sendverclient/<int:id>',views.sendverclient,name="sendverclient"),



    path('verifytestimonial/',views.verifytestimonial,name="verifytestimonial"),
    path('editverificationtestimonial/<int:id>',views.editverificationtestimonial,name="editverificationtestimonial"),
    path('deletetestimonial/<int:id>',views.deletetestimonial,name="deletetestimonial"),
    path('approvetestimonial/<int:id>',views.approvetestimonial,name="approvetestimonial"),
    path('sendvertestimonial/<int:id>',views.sendvertestimonial,name="sendvertestimonial"),
    
    
    path('verifyexperience/',views.verifyexperience,name="verifyexperience"),
    path('editverificationexperience/<int:id>',views.editverificationexperience,name="editverificationexperience"),
    path('deleteexperience/<int:id>',views.deleteexperience,name="deleteexperience"),
    path('approveexperience/<int:id>',views.approveexperience,name="approveexperience"),
    path('sendverxperience/<int:id>',views.sendverxperience ,name="sendverxperience"),
    
    path('verifyachievements/',views.verifyachievements,name="verifyachievements"),
    path('editverificationachievements/<int:id>',views.editverificationachievements,name="editverificationachievements"),
    path('deleteachievements/<int:id>',views.deleteachievements,name="deleteachievements"),
    path('approveachievements/<int:id>',views.approveachievements,name="approveachievements"),
    path('sendverachievements/<int:id>',views.sendverachievements,name="sendverachievements"),
    
    path('verifyexpertise/',views.verifyexpertise,name="verifyexpertise"),
    path('editverificationexpertise/<int:id>',views.editverificationexpertise,name="editverificationexpertise"),
    path('deleteexpertise/<int:id>',views.deleteexpertise,name="deleteexpertise"),
    path('approveexpertise/<int:id>',views.approveexpertise,name="approveexpertise"),
    path('sendverexpertise/<int:id>',views.sendverexpertise,name="sendverexpertise"),


    path('verifyprojects/',views.verifyprojects,name="verifyprojects"),
    path('editverificationprojects/<int:id>',views.editverificationprojects,name="editverificationprojects"),
    path('deleteprojects/<int:id>',views.deleteprojects,name="deleteprojects"),
    path('approveprojects/<int:id>',views.approveprojects,name="approveprojects"),
    path('sendverprojects/<int:id>',views.sendverprojects,name="sendverprojects"),


    #### jquery autocomplete company name #####

    path('company_autocomplete/',views.company_autocomplete,name="company_autocomplete"),
    path('client_autocomplete/',views.client_autocomplete,name="client_autocomplete"),
    path('search_auto/',views.search_auto,name="search_auto"),
    
    
    path('postreports/',views.postreport,name="postreports"),



]
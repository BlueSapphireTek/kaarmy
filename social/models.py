from django.db import models

# Create your models here.
from byhand.models import CustomUser,UserExtend
from byhand.models import Bio
from mimetypes import guess_type



class Post(models.Model):
    
    PRIVACY_CHOICE = (('1', 'Public'), ('2', 'Friends'), ('3', 'Private'),)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    userextend = models.ForeignKey(UserExtend, on_delete=models.CASCADE, blank=True, null=True)
    caption = models.CharField(max_length=500,null=True,blank = True)

    date = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=1000,null=True)
    file = models.FileField(upload_to='media',null=True,blank = True)
    likes = models.IntegerField(default = 0)
    comments =models.IntegerField(default = 0)
    is_deleted =models.IntegerField(default = 0)
    privacy = models.CharField(
        choices=PRIVACY_CHOICE, max_length=20, default='1')
    
    
    def file_type_html(self):
        
        type_tuple = guess_type(self.file.url, strict=True)
        if (type_tuple[0]).__contains__("image"):
            
            return "image"
        elif (type_tuple[0]).__contains__("video"):
            
            return "video"
        
    
    class Meta:
        get_latest_by = ['date']
        ordering = ['-date', ]


    def __str__(self):
        return str(self.id)

    @property
    def cmtset(self):
        commentss = self.comment_set.all()
        # print(commentss)
        return commentss

    @property
    def cmtcount(self):
        commentss = self.comment_set.count()
        return commentss

    @property
    def likecount(self):
        likes = self.like_set.count()
        return likes
    
    @property
    def reportcount(self):
        reports = self.report_set.count()
        return reports


class Like(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True,)



class Comment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True)
    bio = models.ForeignKey(Bio, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateTimeField(auto_now=True)
    
class Report(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True)
    reporter = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    content = models.CharField(max_length=50,null=True)

class Enquiry(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateTimeField(auto_now=True)


class Working(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank = True,null = True)
    day = models.CharField(max_length= 50,null = True)
    availability = models.BooleanField(default =False)
    start_time = models.TimeField(null = True)
    end_time = models.TimeField(null = True)
    breaktimef_start = models.TimeField(null = True)
    breaktimef_end = models.TimeField(null = True)
    breaktimes_start = models.TimeField(null = True)
    breaktimes_end = models.TimeField(null = True)

class About(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank = True,null = True)
    about= models.CharField(max_length= 2000)


###############inlineformset#########################################
class Achievement(models.Model):
    user  = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank = True,null = True)
    name = models.CharField(max_length=200,null=True)
class Projects(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank = True,null = True, related_name = "uuserp")
    auth = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True, null=True, related_name = "auserp")
    authname = models.CharField(max_length=250,null= True)
    project_name = models.CharField(max_length = 100,null = True)
    company = models.CharField(max_length = 100,null = True)
    is_approved = models.IntegerField(default=0)
    is_rejected = models.IntegerField(default=0)
    is_requested = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
class Cexepertise(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    profession = models.CharField(max_length =100,null = True)
    year = models.IntegerField(null = True)

class Expertise(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True, null=True, related_name = "eusere")
    auth = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True, null=True, related_name = "ausere")
    authname = models.CharField(max_length=250,null= True)
    profession = models.CharField(max_length = 500,null = True)
    expertisein = models.CharField(max_length = 500,null = True)
    years = models.FloatField(null = True)
    description = models.CharField(max_length = 5000,null = True,blank = True)
    is_approved = models.IntegerField(default=0)
    is_rejected = models.IntegerField(default=0)
    is_requested = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
class Achievements(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True ,related_name = "uusera")
    auth = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True, null=True, related_name = "ausera")
    authname = models.CharField(max_length=250,null= True)
    title = models.CharField(max_length = 250,null= True)
    description = models.CharField(max_length = 5000,null= True,blank = True)
    is_approved = models.IntegerField(default=0)
    is_rejected = models.IntegerField(default=0)
    is_requested = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

class Experience(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,related_name = "user")
    fromyear = models.DateField(null = True)
    toyear = models.DateField(null = True)
    company_name = models.CharField(max_length = 50,null = True)
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True,related_name = "company")
    exp_keywords = models.CharField(max_length = 500,null = True)
    exp_detail = models.CharField(max_length = 500,null = True,blank=True)
    comments = models.CharField(max_length = 500,null = True, blank=True)
    responsibily = models.CharField(max_length = 500,null = True, blank=True)
    expimage = models.ImageField(upload_to='media', null=True, blank=True)
    is_approved = models.IntegerField(default=0)
    is_rejected = models.IntegerField(default=0)
    is_requested = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True) 

class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,related_name = "userc")
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,related_name = "client")
    clientname = models.CharField(max_length = 500,null = True)
    clientimage = models.FileField(upload_to='media', null=True, blank=True)
    client_description = models.CharField(max_length = 5000,null = True)
    is_approved = models.IntegerField(default=0)
    is_rejected = models.IntegerField(default=0)
    is_requested = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

class Testimonial(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="usert")
    testuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="testuser")
    testimonial_name = models.CharField(max_length= 500,null=True, blank=True)
    testimonial_image = models.ImageField(upload_to='media', null=True, blank=True)
    testimonial_description = models.CharField(max_length=5000, null=True)
    is_approved = models.IntegerField(default=0)
    is_rejected = models.IntegerField(default=0)
    is_requested = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

class Certificate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="usercer")
    authority = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="authority")
    certificate_name = models.CharField(max_length = 5000,null = True)
    certificate_id = models.CharField(max_length = 500,null= True)
    certificate_image = models.ImageField(upload_to='media', null=True, blank=True)
    certificate_description = models.CharField(max_length = 5000,null = True)
    company_name = models.CharField(max_length = 5000,null = True)
    is_approved = models.IntegerField(default = 0)
    is_rejected = models.IntegerField(default=0)
    is_requested = models.IntegerField(default = 0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date']

class Branch(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.CharField(max_length = 50,null = True)
    branchaddress = models.CharField(max_length = 5000,null = True)
    

class Location(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    place = models.CharField(max_length=500,null=True)
    


class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'),(3,'Certifiacte'),(4,'follow'),(5,'endorse'),(6,'connected'))

    post = models.ForeignKey(Post, on_delete=models.CASCADE ,related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

class Brousher(models.Model):

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True,null = True)
    brousher = models.ImageField(upload_to='media', null=True, blank=True)

class Image(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True,null = True)
    image = models.ImageField(upload_to='media', null=True, blank=True)

class Documents(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    DOCS = models.FileField(upload_to='media',null = True)

class Cards(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    card  = models.FileField(upload_to='media',null = True)




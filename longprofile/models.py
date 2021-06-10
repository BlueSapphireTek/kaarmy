from django.db import models
from byhand.models import CustomUser


# Create your models here.
class Company_card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    front_img = models.ImageField(upload_to='media',null=True,blank=True)
    back_img = models.ImageField(upload_to='media',null=True,blank=True)
    company_name = models.CharField(max_length=150,null=True,blank=True)
    services = models.CharField(max_length=50,null=True,blank=True)
    mobile = models.IntegerField(null=True,blank=True)
    email = models.CharField(max_length=150,null=True,blank=True)
    whatsapp = models.IntegerField(null=True,blank=True)
    location = models.CharField(max_length=150,null=True,blank=True)
    company_name = models.CharField(max_length=150,null=True,blank=True)
    company_location = models.CharField(max_length=150,null=True,blank=True)
    website = models.CharField(max_length=150,null=True,blank=True)
    aditional_details = models.CharField(max_length=150,null=True,blank=True)
    update_at = models.DateTimeField(auto_now=True)
class Personal_card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    front_img = models.ImageField(upload_to='media',null=True,blank=True)
    back_img = models.ImageField(upload_to='media',null=True,blank=True)
    company_name = models.CharField(max_length=150,null=True,blank=True)
    services = models.CharField(max_length=50,null=True,blank=True)
    mobile = models.IntegerField(null=True,blank=True)
    email = models.CharField(max_length=150,null=True,blank=True)
    whatsapp = models.IntegerField(null=True,blank=True)
    location = models.CharField(max_length=150,null=True,blank=True)
    company_name = models.CharField(max_length=150,null=True,blank=True)
    company_location = models.CharField(max_length=150,null=True,blank=True)
    website = models.CharField(max_length=150,null=True,blank=True)
    aditional_details = models.CharField(max_length=150,null=True,blank=True)
    update_at = models.DateTimeField(auto_now=True)
class Follow2(models.Model):
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="who_follows2")
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,related_name="who_following2")
    follow_time = models.DateTimeField(auto_now=True)
class Endorse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="who_endorsing")
    liked_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,related_name="who_liked")
    follow_time = models.DateTimeField(auto_now=True)
class Connection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="who_requested")
    connected_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,related_name="who_connected")
    connection = models.IntegerField(default= 0)
    connected_time = models.DateTimeField(auto_now=True)
class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    rated_person = models.IntegerField()
    rating = models.FloatField()
class CreateEvent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media')
    created_on = models.DateTimeField(auto_now=True)
class SavedEvent(models.Model):
    savedperson = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    event = models.ForeignKey(CreateEvent, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
class CreateEnquiry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="snd")
    enquired_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,related_name="reciver")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now=True)
class SavedEnquiry(models.Model):
    savedperson = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    enquiry = models.ForeignKey(CreateEnquiry, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
class CreateAppoinment(models.Model):
    
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    created_on = models.DateTimeField(auto_now=True)
class CreateAppoinment2(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="snder")
    enquired_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,related_name="company1")
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    dateandtime = models.DateTimeField()
    active = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now=True)
class Aboutdetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=900)
    created_on = models.DateTimeField(auto_now=True)
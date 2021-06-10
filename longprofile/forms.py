from django import forms
from longprofile.models import *


# class Company_cardForm(forms.ModelForm):
#     class Meta:
#         model = Company_card
#         fields = ('name','email','job','company_name','address1','address2','address3','phone1','phone2','logo')
# class Personal_cardForm(forms.ModelForm):
#     class Meta:
#         model = Personal_card
#         fields = ('name','email','job','company_name','address1','address2','address3','phone1','phone2','logo','photo')
class CreateEventForm(forms.ModelForm):
    class Meta:
        model = CreateEvent
        fields = ('name','description','image')
class CreateEnquiryForm(forms.ModelForm):
    class Meta:
        model = CreateEnquiry
        fields = ('title','description')
class CreateAppoinmentForm(forms.ModelForm):
    class Meta:
        model = CreateAppoinment
        fields = ('name','purpose','description','date','time')
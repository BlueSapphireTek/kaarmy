from django import forms

from social.models import Post,Achievements,Working,About,Expertise,Projects,Experience,Client,Testimonial,Certificate,Comment,Branch




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption','file')
        
        

class WorkingForm(forms.ModelForm):
    class Meta:
        model = Working
        fields = ('day','availability','start_time','end_time','breaktimef_start','breaktimef_end','breaktimes_start','breaktimes_end')

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ('about',)

class ExpertiseForm(forms.ModelForm):
    class Meta:
        model = Expertise
        fields = ('profession','expertisein','years','description')

class AchievementsForm(forms.ModelForm):
    class Meta:
        model = Achievements
        fields = ('title','description')
class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ('project_name','company')

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ('fromyear','toyear','exp_keywords','exp_detail','comments','responsibily')

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('clientimage','client_description')

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('testimonial_image','testimonial_description')

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('certificate_name','certificate_id','certificate_image','certificate_description',)

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('branch', 'branchaddress',)





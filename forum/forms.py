from django import forms
from django.contrib.auth.models import User
from forum.models import Forum, Yorumforum, ReportForum

class addforumForm(forms.ModelForm):
    class Meta:
        model=Forum
        fields=["title", "oyun", "soru"]
    
class addYorumForm(forms.ModelForm):
    class Meta:
        model=Yorumforum
        fields=["yorum"]

class addReportForm(forms.ModelForm):
    class Meta:
        model=ReportForum
        fields=["sorun"]

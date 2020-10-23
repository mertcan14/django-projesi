from django import forms
from haberler.models import Haber, YorumHaber, AddReportHaber
class addhaberForm(forms.ModelForm):
    class Meta:
        model=Haber
        fields=["baslik", "content", "tags", "haber_image"]
class addyorumForm(forms.ModelForm):
    class Meta:
        model=YorumHaber
        fields=["yorum"]
class addreportForm(forms.ModelForm):
    class Meta:
        model=AddReportHaber
        fields=["sorun"]
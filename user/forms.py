from django import forms
from django.contrib.auth.models import User
from user.models import Profil
class kayitForm(forms.Form):
    username=forms.CharField(
        label="Username",
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder':'username'})
    )
    email=forms.EmailField(
        label="E-Mail",
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder':'e-mail'})
    )
    password=forms.CharField(
        label="Şifre",
        max_length=20,
        min_length=8,
        widget=forms.PasswordInput,
    )
    tekrar=forms.CharField(
        label="Şifre Tekrar",
        max_length=20,
        min_length=8,
        widget=forms.PasswordInput
    )

    def clean(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        tekrar=self.cleaned_data.get("tekrar")
        email=self.cleaned_data.get("email")

        if password and tekrar and password!=tekrar:
            raise forms.ValidationError("Parola Uyuşmuyor..")

        values={
            "username":username,
            "password":password,
            "email":email
        }
        return values

class girisForm(forms.Form):
    username=forms.CharField(
        label="Username",
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder':'username'})
    )
    password=forms.CharField(
        label="Şifre",
        max_length=20,
        min_length=8,
        widget=forms.PasswordInput,
    )

class updateUserForms(forms.ModelForm):
    class Meta:
        model= User
        fields=["username", "first_name", "last_name","email"]

class updateProfileForms(forms.ModelForm):
    class Meta:
        model= Profil
        fields=["hakkında","location","dogum_gunu", "cinsiyet", "user_image"]
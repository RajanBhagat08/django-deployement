from django import forms
from django.contrib.auth.models import User
from EAD_app.models import User_info
from EAD_app.models import venue

class userform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=("email","username","password")

class NewuserForm(forms.ModelForm):

    class Meta:
        model = User_info
        fields=("description",)

class booking_form_secy(forms.ModelForm):
    class Meta:
        model=venue
        fields=("event_name","associated_club","date","requested_venue_secy")

class booking_form_student(forms.ModelForm):
    class Meta:
        model=venue
        fields=("event_name","date","requested_venue_student")

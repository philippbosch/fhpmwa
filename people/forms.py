from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from fhpmwa.people.models import MOBILE_DEVICE_CHOICES, COMPUTER_OS_CHOICES

class UserForm(forms.Form):
    # username = forms.CharField(max_length=30, label=_("Username"))
    first_name = forms.CharField(max_length=30, label=_("Vorname"))
    last_name = forms.CharField(max_length=30, label=_("Nachname"))
    email = forms.EmailField(label=_("E-Mail"))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, label=_("Passwort"))
    matric_no = forms.CharField(max_length=20, label=_("Matrikelnummer"))
    zipcode = forms.CharField(max_length=5, label=_("PLZ"))
    photo = forms.ImageField(required=False, label=_("Foto"))
    mobile_device = forms.ChoiceField(required=True, label=_("Mobile Device"), choices=MOBILE_DEVICE_CHOICES, widget=forms.RadioSelect)
    mobile_device_other = forms.CharField(max_length=100, label=_("Anderes"), required=False)
    computer_os = forms.ChoiceField(required=True, label=_("Betriebsystem"), choices=COMPUTER_OS_CHOICES, widget=forms.RadioSelect)

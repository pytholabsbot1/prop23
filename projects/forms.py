from django.forms import (
    ModelForm,
    fields,
    Form,
    CharField,
    Textarea,
    TextInput,
    ChoiceField,
    Select,
)
from .models import Enquiry


GEEKS_CHOICES = (
    ("",""),
    ("1BHK Studio", "1BHK Studio"),
    ("2BHK Studio", "2BHK Studio"),
    ("3BHK Flats", "3BHK Flats"),
    ("4BHK Duplex Villa", "4BHK Duplex Villa"),
    ("5BHK Duplex Villa", "5BHK Duplex Villa"),
)


class EnquiryForm(Form):
    name = CharField(max_length=100, widget=TextInput(attrs={"class": "form-control"}))
    phone = CharField(max_length=100, widget=TextInput(attrs={"class": "form-control"}))
    email = CharField(max_length=100, widget=TextInput(attrs={"class": "form-control"}))
    msg = CharField(max_length=100, widget=TextInput(attrs={"class": "form-control"}))


class BrochureForm(Form):
    name = CharField(
        max_length=100, required=True, widget=TextInput(attrs={"class": "swal2-input"})
    )
    phone = CharField(
        max_length=100, required=True, widget=TextInput(attrs={"class": "swal2-input"})
    )
    email = CharField(max_length=100, widget=TextInput(attrs={"class": "swal2-input"}))
    interested_in = ChoiceField(
        required=True,
        choices=GEEKS_CHOICES,
        widget=Select(attrs={"class": "swal2-input"}),
    )

    # class META:

    #     widgets = {
    #         "interested_in": ChoiceField(attrs={"class": "swal2-input"}),
    #     }

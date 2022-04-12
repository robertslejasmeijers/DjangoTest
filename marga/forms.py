from django import forms

class Searchdb(forms.Form):
    search = forms.CharField(label="search", required=False, max_length=200)
    labels = {"search": ""}
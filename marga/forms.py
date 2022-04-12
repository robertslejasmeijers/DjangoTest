from django import forms

class Searchdb(forms.Form):
    search = forms.CharField(label="search", max_length=200)

from django import forms

class Searchdb(forms.Form):
    search = forms.CharField(label="Meklēt", required=False, max_length=200)
    
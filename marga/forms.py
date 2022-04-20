from django import forms

class Searchdb(forms.Form):
    name = forms.CharField(label="", required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Meklēt preci', 'class': 'form-inline', 'style': 'padding-left: 8px;'}))
    
class Addurl(forms.Form):
    name = forms.CharField(label="", required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Pievienot saiti no Rimi vai Barbora', 'class': 'form-control w-50'}))	

class Deleteurl(forms.Form):
    name = forms.CharField(label="", required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Lai dzēstu saiti, ievadi ID (lai dzēstu visas, ievadi "0"):', 'class': 'form-control w-25'}))	
    
from django import forms
from .models import Previsao

class DadosForm(forms.Form):
    N = forms.FloatField()
    P = forms.FloatField()
    K = forms.FloatField()
    pH = forms.FloatField()
    EC = forms.FloatField()
    OC = forms.FloatField()
    S = forms.FloatField()
    Zn = forms.FloatField()
    Fe = forms.FloatField()
    Cu = forms.FloatField()
    Mn = forms.FloatField()

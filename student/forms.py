from django import forms

class JoinClassForm(forms.Form):
    code = forms.CharField(max_length=7, label="Class Code")
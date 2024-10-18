# from django import forms

# class InterestForm(forms.Form):
#     email = forms.EmailField(label="Enter your E-mail here..", required=True)
#     text = forms.CharField(widget=forms.Textarea, required=False, label="Add a message (optional)..")

from django import forms

class InterestForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label="Enter your E-mail here..",  # Keep the label
        widget=forms.EmailInput(attrs={
            'placeholder': 'enter your email...',  # Different placeholder text
            'class': 'form-control'
        })
    )
    text = forms.CharField(
        required=False,
        label="Add a message (optional)..",  # Keep the label
        widget=forms.Textarea(attrs={
            'placeholder': 'optional message...',  # Different placeholder text
            'class': 'form-control',
            'rows': 4
        })
    )


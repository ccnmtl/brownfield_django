from django import forms



class CreateClassForm(forms.Form):
    '''This is a form class that will be
    used with ajax to create new classes.'''
    sender = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(max_length=500, required=True,
                              widget=forms.Textarea)
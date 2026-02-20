from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class' : 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm ur password',
        'class' : 'form-control',
    }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password :
            raise forms.ValidationError(
                "ithokke sredhiknde ambane password match avanilla "         # viewsil check chynnam or code comment akkit it else inte avidey
            )
        

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='peru parayada kuttah'
        self.fields['last_name'].widget.attrs['placeholder']='nigdey daddy girija'
        for feild in self.fields:
            self.fields[feild].widget.attrs['class'] = 'form-control'

    



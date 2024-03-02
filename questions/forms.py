from django import forms
from questions.models import MyUser, Questions
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'profile_pic',
                  'password1', 'password2']

class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Questions
        fields=['description', 'image']
        widgets = {'description': forms.Textarea(attrs={'class':'form-control'}),
                    'image':forms.FileInput(attrs={'class':'form-select'})

                    }


class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))


from django import forms
from .models import Profile
from .models import Feedback

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'category', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 h-32 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }

class CustomSignUpForm(forms.Form):
    name = forms.CharField(label="Full Name", widget=forms.TextInput(attrs={
        'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
    }))

# Engineer Form
class EngineerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone', 'license_number', 'specialization', 'experience', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(EngineerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['specialization'].required = True

# Contractor Form
class ContractorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone', 'specialization', 'experience', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(ContractorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['specialization'].required = True

# worker Form (now includes specialization)
class workerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone', 'specialization', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(workerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['specialization'].required = True

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Feedback', 'rows': 4}),
        }

class YourFormName(forms.Form):
    phone = forms.CharField(max_length=10, min_length=10)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone
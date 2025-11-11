from django import forms
from a_core.models import UserProfile
from django.contrib.auth import get_user_model 

User = get_user_model()

class UserProfileForm(forms.ModelForm):

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us a little bit about yourself...'}),
        required=False,
        label='Biography'
    )
    
    profile_picture = forms.ImageField(
        label='Profile Picture (Optional)',
        required=False,
        help_text='Upload your profile picture.'
    )

    class Meta:
        model = UserProfile
        
        fields = ['bio', 'profile_picture', 'age', 'location']
        
        widgets = {
            'age': forms.NumberInput(attrs={'placeholder': 'Your age'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country or general location'}),
        }
        labels = {
            'age': 'Age (Years)',
            'location': 'Location',
        }
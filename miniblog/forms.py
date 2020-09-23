from django import forms
from miniblog.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('country', 'phone_number', 'birth_date', 'bio', )
        # widgets = {
        #     'birth_date': forms.DateInput(format=('%d-%m-%Y'), attrs={'type': 'date'}),
        # }

    def save(self, user=None):
        profile = super(ProfileForm, self).save(commit=False)
        if user:
            profile.user = user
        profile.save()
        return profile


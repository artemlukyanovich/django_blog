from django import forms
from miniblog.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')

    def save(self, user=None):
        profile = super(ProfileForm, self).save(commit=False)
        if user:
            profile.user = user
        profile.save()
        return profile
from django import forms
from .models import Creator, Team, Member, TeamRequest


class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['name', 'money']


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'creator']


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'stamina', 'team']


class TeamRequestForm(forms.ModelForm):
    class Meta:
        model = TeamRequest
        fields = ['member', 'team']


class ProcessTeamRequestsForm(forms.Form):
    max_members = forms.IntegerField(label='Maximum members', min_value=1, required=True)
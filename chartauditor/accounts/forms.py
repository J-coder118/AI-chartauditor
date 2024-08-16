from django import forms
from chartauditor.accounts.models import CompanyInformation
from django.contrib.auth.forms import SetPasswordForm
from chartauditor.accounts.models import FacultyOption


class CompanyInfoForm(forms.ModelForm):
    DEFAULT_OPTION = [('', 'Select Any Option')]
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        # required=True
    )
    accreditation = forms.ChoiceField(
        choices=DEFAULT_OPTION + list(CompanyInformation.ACCREDITATION_OPTIONS),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    state_licence = forms.ChoiceField(
        choices=DEFAULT_OPTION + list(CompanyInformation.STATE_COMPLIANCE),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    facility_type = forms.ModelMultipleChoiceField(
        queryset=FacultyOption.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control multipleSelect'
        })
    )

    class Meta:
        model = CompanyInformation
        fields = ['facility_name', 'state_licence', 'accreditation', 'accept_insurance', 'facility_type']

    def __init__(self, *args, **kwargs):
        super(CompanyInfoForm, self).__init__(*args, **kwargs)

        self.fields['facility_name'].widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
        self.fields['accept_insurance'].widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )

        if self.instance.user_id:
            self.fields['first_name'].initial = self.instance.user.first_name

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        if first_name and self.instance.user_id:
            self.instance.user.first_name = first_name
            self.instance.user.save()
        return cleaned_data


class CompanyInfoCreationForm(forms.ModelForm):
    DEFAULT_OPTION = [('', 'Select Any Option')]

    accreditation = forms.ChoiceField(
        choices=DEFAULT_OPTION + list(CompanyInformation.ACCREDITATION_OPTIONS),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    state_licence = forms.ChoiceField(
        choices=DEFAULT_OPTION + list(CompanyInformation.STATE_COMPLIANCE),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    facility_type = forms.ModelMultipleChoiceField(
        queryset=FacultyOption.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control multipleSelect'
        })
    )

    class Meta:
        model = CompanyInformation
        fields = ['facility_name', 'state_licence', 'accreditation', 'accept_insurance', 'facility_type']

    def __init__(self, *args, **kwargs):
        super(CompanyInfoCreationForm, self).__init__(*args, **kwargs)

        self.fields['facility_name'].widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
        self.fields['accept_insurance'].widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )


class ChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control password-field',
            'id': 'newPassword',
            'name': 'newPassword',
            'placeholder': "********",
        })
    )
    new_password2 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control password-field',
            'id': 'password',
            'name': 'cnfrmPassword',
            'placeholder': "********",
        })
    )

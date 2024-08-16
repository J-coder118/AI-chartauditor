from django import forms
from chartauditor.pdf_wrapper.models import ChartChecker


class ChartCheckerForm(forms.ModelForm):
    DEFAULT_OPTION1 = [('', 'Select Insurance')]
    DEFAULT_OPTION2 = [('', 'Select State')]
    insurance_compliance = forms.ChoiceField(
        choices=DEFAULT_OPTION1 + list(ChartChecker.COMPLIANCE),
        widget=forms.Select(
            attrs={
                'class': 'switchSecSelect',
                'id': 'insuranceOptions'
            }
        )
    )
    state_compliance = forms.ChoiceField(
        choices=DEFAULT_OPTION2 + list(ChartChecker.STATE_COMPLIANCE),
        widget=forms.Select(
            attrs={
                'id': 'stateOption',
                'class': 'switchSecSelect',
            }
        ),
        required=False
    )

    class Meta:
        model = ChartChecker
        fields = [
            'chart', 'is_report_emailed', 'is_state_compliance', 'state_compliance', 'is_CARF_compliance',
            'is_marked_cover_letter', 'is_commission_compliance', 'insurance_compliance', 'is_insurance_compliance',
        ]

    def __init__(self, *args, **kwargs):
        super(ChartCheckerForm, self).__init__(*args, **kwargs)
        self.fields['chart'].widget = forms.FileInput(
            attrs={
                'id': 'fileInput',
                'class': 'file-input',
            }
        )
        self.fields['is_report_emailed'].widget = forms.CheckboxInput(
            attrs={
                'class': 'similarInputGroup radioOne',
            }
        )
        self.fields['is_state_compliance'].widget = forms.CheckboxInput(
            attrs={
                'class': 'similarInputGroup radioOne',
                'id': "stateList",
            }
        )
        self.fields['is_CARF_compliance'].widget = forms.CheckboxInput(
            attrs={
                'class': 'similarInputGroup radioOne',
            }
        )
        self.fields['is_marked_cover_letter'].widget = forms.CheckboxInput(
            attrs={
                'class': 'similarInputGroup radioOne',
            }
        )
        self.fields['is_commission_compliance'].widget = forms.CheckboxInput(
            attrs={
                'class': 'similarInputGroup radioOne',
            }
        )
        self.fields['is_insurance_compliance'].widget = forms.CheckboxInput(
            attrs={
                'class': 'similarInputGroup radioOne',
                'id': "isInsurance",
            }
        )
        self.fields['insurance_compliance'].required = False

    def clean(self):
        cleaned_data = super().clean()
        chart = cleaned_data.get('chart')
        is_state_compliance = cleaned_data.get('is_state_compliance')
        state_compliance = cleaned_data.get('state_compliance')
        is_insurance_compliance = cleaned_data.get('is_insurance_compliance')
        insurance_compliance = cleaned_data.get('insurance_compliance')

        file_size_in_mb = None
        if chart:
            file_size_in_bytes = chart.size
            file_size_in_mb = file_size_in_bytes / (1024 * 1024)

        if file_size_in_mb is not None and file_size_in_mb > 300:
            raise forms.ValidationError('Cannot upload more than 300 mbs.')

        if is_state_compliance and not state_compliance:
            raise forms.ValidationError('please choose an option from state compliance.')

        if is_insurance_compliance and not insurance_compliance:
            raise forms.ValidationError('please choose an option from insurance compliance.')

        if not chart:
            raise forms.ValidationError('Please select a file first then generate report')

        if not chart.name.endswith(('.zip', '.pdf')):
            raise forms.ValidationError('Chart must be PDF or a Zip of PDFs')

        if not any([cleaned_data.get('is_report_emailed'),
                    cleaned_data.get('is_state_compliance'),
                    cleaned_data.get('is_CARF_compliance'),
                    cleaned_data.get('is_marked_cover_letter'),
                    cleaned_data.get('is_insurance_compliance'),
                    cleaned_data.get('is_commission_compliance')]):
            raise forms.ValidationError('Please select at least one Chart Auditor.')

        return cleaned_data

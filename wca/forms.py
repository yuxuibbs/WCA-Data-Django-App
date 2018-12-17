from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from wca.models import Person
from wca.models import Result


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'submit'))

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        labels = {
            'pos': 'Position',
            'value1': 'Solve #1',
            'value2': 'Solve #2',
            'value3': 'Solve #3',
            'value4': 'Solve #4',
            'value5': 'Solve #5'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'submit'))


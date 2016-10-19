from django import forms
from tmmu.models import Input

class InputForm(forms.ModelForm):
    input1  = forms.FloatField(
        required=True, 
        label="Cnisin Value"
        #max_value=0, 
        #min_value=100,
        )
    input2  = forms.FloatField(
        required=True,
        label="Time Value"
        #max_value=0, 
        #min_value=100,
        )

    class Meta:
        model = Input
        fields =('input1', 'input2',)


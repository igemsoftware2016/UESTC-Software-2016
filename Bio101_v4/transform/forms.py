from django import forms
from .models import Encode, Decode, Edit

class EncodeForm(forms.ModelForm):
	encode_token= forms.CharField(max_length=256, 
			widget=forms.PasswordInput(),
			required = True,
			label = "Please enter a secret token.",
			help_text="max. 256 characters."
			)
	encode_file = forms.FileField( 
			label="Choose a file to encode.",
			required = True,
			max_length=256,
			help_text="max. 5 MiB (megabytes).",
			)
	class Meta:
		model = Encode
		fields= ('encode_token', 'encode_file',)

class DecodeForm(forms.ModelForm):
	decode_token= forms.CharField(max_length=256, 
			widget=forms.PasswordInput(),
			required = True,
			label = "Please enter your token to decrypt.",
			help_text="max. 256 characters."
			)
	decode_file = forms.FileField( 
			label="Choose a sequence file to decode.",
			required = True,
			max_length=256,
			help_text="max. 5 MiB (megabytes).",
			)
	class Meta:
		model = Decode
		fields= ('decode_token', 'decode_file',)


class EditForm(forms.ModelForm):
	edit_fragment=forms.CharField(
		max_length=145,
		required = True,
		widget=forms.Textarea(),
		)
	edit_token = forms.CharField(
		widget=forms.PasswordInput(),
		required = True,
		max_length=256,
		)
	class Meta:
		model = Edit
		fields=('edit_fragment', 'edit_token',)
			

from django import forms
from sportapp.models import Register
from dashboard.models import Addaccounttype, Agentusercreate


class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterUpdateForm(forms.ModelForm):

	# acc_type = forms.ModelChoiceField(queryset=Addaccounttype.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

	class Meta:
		model = Register
		fields = (
			'fname', 'lname', 'uname', 'email', 'country', 'address', 'mob', 'dob', 'acc_type', 'acc_limit', 'demo_acc_limit'
		)
		widgets = {
			'fname': forms.TextInput(
				attrs={
					'class': 'form-control'
				},
			),
			'lname': forms.TextInput(
				attrs={
					'class': 'form-control'
				}
			),
			'uname': forms.TextInput(
				attrs={
					'class': 'form-control'
				}
			),
			'email': forms.EmailInput(
				attrs={
					'class': 'form-control'
				}
			),
			'country': forms.TextInput(
				attrs={
					'class': 'form-control'
				}
			),
			'address': forms.TextInput(
				attrs={
					'class': 'form-control'
				}
			),
			# 'mob': forms.NumberInput(
			# 	attrs={
			# 		'class': 'form-control'
			# 	}
			# ),
			'dob': DateInput(
				attrs={
					'class':'form-control'
				},
			),
            # 'acc_limit': forms.NumberInput(
			# 	attrs={
			# 		'class': 'form-control'
			# 		}
			# 	),			
            # 'demo_acc_limit': forms.NumberInput(
			# 	attrs={
			# 		'class': 'form-control'
			# 		}
			# 	),
			}

	# def clean(self):

	# 	super(RegisterUpdateForm, self).clean()

	# 	ac_lim = self.cleaned_data.get('acc_limit')
	# 	dem_ac_lim = self.cleaned_data.get('demo_acc_limit')
	# 	email = self.cleaned_data.get('email')

	# 	if int(ac_lim) < 4:
	# 		self._errors['acc_limit'] = self.error_class(['Min 4 required for validation'])
	# 	if int(dem_ac_lim) < 2:
	# 		self._errors['demo_acc_limit'] = self.error_class(['Min 2 required for validation'])

	# 	return self.cleaned_data
	
	# def clean_email(self):

	# 	email = self.cleaned_data.get('email')

	# 	try:
	# 		match = Register.objects.get(email=email)
	# 	except Register.DoesNotExist:
	# 	# Unable to find a user, this is fine
	# 		return email

	# 	# A user was found with this as a username, raise an error.
	# 	raise forms.ValidationError('This email address is already in use.')


class AgentUserCreateForm(forms.ModelForm):
	class Meta:
		model = Agentusercreate
		fields = '__all__'
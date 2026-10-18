from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


class CriarContaForm(UserCreationForm):

    email = forms.EmailField(
        label="E-mail",
        required=True
    )

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado."
            )

        return email

class FormHomePage(forms.Form):
    email = forms.EmailField(label=False)
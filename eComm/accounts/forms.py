from django import forms


class LoginForm(forms.Form):
    username    = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Username",
        }
    ))
    password    = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Password",
        }
    ))


class RegisterForm(forms.Form):
    username    = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Username",
        }
    ))
    email       = forms.EmailField(widget=forms.EmailInput(
        attrs= {
            'class': "form-control",
            'placeholder': "Email",
        }
    ))
    password    = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Password",
        }
    ))
    password2   = forms.CharField(label= "Confirm Password", widget=forms.PasswordInput(
        attrs = {
            'class': "form-control",
            'placeholder': "Confirm Password",
        }
    ))


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gamil.com")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password must match.")
        return data


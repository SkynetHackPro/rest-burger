from django import forms
from django.contrib import admin

from django.apps import apps

from burgershop.models import User

app = apps.get_app_config('burgershop')


class UserForm(forms.ModelForm):
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'is_staff', 'is_superuser', 'is_dealer')
        model = User

    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(admin.ModelAdmin):
    form = UserForm


admin.site.register(User, CustomUserAdmin)

# for model_name, model in app.models.items():
#     if model_name != 'user':
#         admin.site.register(model)
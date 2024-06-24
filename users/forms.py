from django import forms
from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'floating-input form-control','placeholder':' '})

    class Meta:
        model = get_user_model()
        fields = ['username','email','password1','password2']
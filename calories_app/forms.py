"""Forms used in the calories application."""

# pylint: disable=relative-beyond-top-level

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Food, Profile


# pylint: disable=too-many-ancestors, too-few-public-methods
class CreateUserForm(UserCreationForm):
    """Form used for creating a new user."""

    class Meta:
        """Meta configuration for CreateUserForm."""

        model = User
        fields = ["username", "email", "password1", "password2"]


# pylint: disable=too-few-public-methods
class SelectFoodForm(forms.ModelForm):
    """Form used to select food items."""

    class Meta:
        """Meta configuration for SelectFoodForm."""

        model = Profile
        fields = ("food_selected", "quantity")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["food_selected"].queryset = Food.objects.filter(person_of=user)


# pylint: disable=too-few-public-methods
class AddFoodForm(forms.ModelForm):
    """Form used to add food items."""

    class Meta:
        """Meta configuration for AddFoodForm."""

        model = Food
        fields = ("name", "quantity", "calorie")


# pylint: disable=too-few-public-methods
class ProfileForm(forms.ModelForm):
    """Form used to update profile calorie goal."""

    class Meta:
        """Meta configuration for ProfileForm."""

        model = Profile
        fields = ("calorie_goal",)
"""Filters for food search functionality."""

# pylint: disable=relative-beyond-top-level

import django_filters
from django_filters import CharFilter

from .models import Food


class FoodFilter(django_filters.FilterSet):  # pylint: disable=too-few-public-methods
    """Filter class for searching food items."""

    food_name = CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="search food items",
    )

    class Meta:
        """Meta configuration for FoodFilter."""

        model = Food
        fields = ["food_name"]

"""Django Models for calories_app. database"""

from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    """Food model."""

    objects = models.Manager()

    name = models.CharField(max_length=200, null=False)
    quantity = models.PositiveIntegerField(null=False, default=0)
    calorie = models.FloatField(null=False, default=0)
    person_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        """Return food name."""
        return str(self.name)


class Profile(models.Model):
    """Profile model."""

    objects = models.Manager()
    person_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    calorie_count = models.FloatField(default=0, null=True, blank=True)
    food_selected = models.ForeignKey(
        Food, on_delete=models.CASCADE, null=True, blank=True
    )
    quantity = models.FloatField(default=0)
    total_calorie = models.FloatField(default=0, null=True)
    date = models.DateField(auto_now_add=True)
    calorie_goal = models.PositiveIntegerField(default=0)
    all_food_selected_today = models.ManyToManyField(
        Food,
        through="PostFood",
        related_name="inventory",
    )

    def save(self, *args, **kwargs):
        """Override save to calculate calories."""
        if self.food_selected is not None:
            amount = self.food_selected.calorie / self.food_selected.quantity
            self.calorie_count = amount * self.quantity
            self.total_calorie = self.calorie_count + self.total_calorie

            calories_app = Profile.objects.filter(
                person_of=self.person_of
            ).last()

            PostFood.objects.create(
                profile=calories_app,
                food=self.food_selected,
                calorie_amount=self.calorie_count,
                amount=self.quantity,
            )

            self.food_selected = None
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        """Return username."""
        return str(self.person_of)


class PostFood(models.Model):
    """PostFood model."""

    objects = models.Manager()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    calorie_amount = models.FloatField(default=0, null=True, blank=True)
    amount = models.FloatField(default=0)
    
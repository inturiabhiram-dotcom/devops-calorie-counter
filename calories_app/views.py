"""Django Views for calories_app."""

# pylint: disable=invalid-name, relative-beyond-top-level

from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from .filters import FoodFilter
from .forms import AddFoodForm, CreateUserForm, ProfileForm, SelectFoodForm
from .models import Food, PostFood, Profile

# home page view
@login_required(login_url="login")
def HomePageView(request):
    """Home page view."""
    calories = Profile.objects.filter(person_of=request.user).last()
    calorie_goal = calories.calorie_goal

    if date.today() > calories.date:
        profile = Profile.objects.create(person_of=request.user)
        profile.save()

    calories = Profile.objects.filter(person_of=request.user).last()

    all_food_today = PostFood.objects.filter(profile=calories)

    calorie_goal_status = calorie_goal - calories.total_calorie
    over_calorie = 0

    if calorie_goal_status < 0:
        over_calorie = abs(calorie_goal_status)

    context = {
        "total_calorie": calories.total_calorie,
        "calorie_goal": calorie_goal,
        "calorie_goal_status": calorie_goal_status,
        "over_calorie": over_calorie,
        "food_selected_today": all_food_today,
    }

    print(context)

    return render(request, "home.html", context)


def RegisterPage(request):
    """User registration page."""
    if request.user.is_authenticated:
        return redirect("home")

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect("login")

    context = {"form": form}
    return render(request, "register.html", context)


def LoginPage(request):
    """Login page."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, "login.html", context)


def LogOutPage(request):
    """Logout user."""
    logout(request)
    return redirect("login")


@login_required
def select_food(request):
    """Select food for the day."""
    person = Profile.objects.filter(person_of=request.user).last()

    food_items = Food.objects.filter(person_of=request.user)

    form = SelectFoodForm(request.user, instance=person)

    if request.method == "POST":
        form = SelectFoodForm(request.user, request.POST, instance=person)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = SelectFoodForm(request.user)

    context = {"form": form, "food_items": food_items}

    print(context)

    return render(request, "select_food.html", context)


def add_food(request):
    """Add food."""
    food_items = Food.objects.filter(person_of=request.user)

    form = AddFoodForm(request.POST)

    if request.method == "POST":
        form = AddFoodForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.person_of = request.user
            profile.save()
            return redirect("add_food")

    else:
        form = AddFoodForm()

    my_filter = FoodFilter(request.GET, queryset=food_items)
    food_items = my_filter.qs

    context = {
        "form": form,
        "food_items": food_items,
        "myFilter": my_filter,
    }

    return render(request, "add_food.html", context)


@login_required
def update_food(request, pk):
    """Update food item."""
    food_items = Food.objects.filter(person_of=request.user)
    food_item = Food.objects.get(id=pk)

    form = AddFoodForm(instance=food_item)

    if request.method == "POST":
        form = AddFoodForm(request.POST, instance=food_item)

        if form.is_valid():
            form.save()
            return redirect("profile")

    my_filter = FoodFilter(request.GET, queryset=food_items)

    context = {
        "form": form,
        "food_items": food_items,
        "myFilter": my_filter,
    }

    return render(request, "add_food.html", context)


@login_required
def delete_food(request, pk):
    """Delete food item."""
    food_item = Food.objects.get(id=pk)

    if request.method == "POST":
        food_item.delete()
        return redirect("profile")

    context = {"food": food_item}

    return render(request, "delete_food.html", context)


@login_required
def ProfilePage(request):
    """User profile page."""
    person = Profile.objects.filter(person_of=request.user).last()

    food_items = Food.objects.filter(person_of=request.user)

    form = ProfileForm(instance=person)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=person)

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = ProfileForm(instance=person)

    some_day_last_week = timezone.now().date() - timedelta(days=7)

    records = Profile.objects.filter(
        date__gte=some_day_last_week,
        date__lt=timezone.now().date(),
        person_of=request.user,
    )

    context = {
        "form": form,
        "food_items": food_items,
        "records": records,
    }

    print(context)

    return render(request, "profile.html", context)
    
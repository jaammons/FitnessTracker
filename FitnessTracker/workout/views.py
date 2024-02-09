from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from users.models import User
from .forms import WorkoutForm
from .utils import save_session, save_custom_workout
from django.db.models import Q

DEFAULT_USER = User.objects.get(username="default")


# Create your views here.
@login_required
def index(request):
    exercises = list(
        Exercise.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )
    workouts = list(
        Workout.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )
    # exercises.extend(list(Exercise.objects.exclude(name__in=exercises).values_list("name", flat=True)))
    # workouts.extend(list(Workout.objects.exclude(name__in=workouts).values_list("name", flat=True)))

    # user.get_module_list()
    modules = ["workout", "cardio", "log", "stats", "settings"]

    return render(
        request,
        "workout/index.html",
        {"modules": modules, "exercises": exercises, "workouts": workouts},
    )
    # "workouts": workouts})


@login_required
def add_exercise(request, exercise, sets=None):
    exercise = {"name": exercise.replace("%20", " ")}
    if sets is None:
        exercise["sets"] = [{"weight": "", "reps": ""}]
    else:
        exercise["sets"] = sets

    return render(request, "workout/exercise.html", {"exercise": exercise})


@login_required
def add_set(request):
    return render(request, "workout/set.html")


@login_required
def select_workout(request, workout_name):
    exercises = Workout.objects.filter(
        Q(name=workout_name.replace("%20", " "), user=request.user)
        | Q(name=workout_name.replace("%20", " "), user=DEFAULT_USER)
    ).first()

    return render(
        request, "workout/workout.html", {"exercises": exercises.config["exercises"]}
    )


@login_required
def save_workout_session(request):
    if request.method == "POST":
        workout_form = WorkoutForm(request.POST)

        if workout_form.is_valid():
            save_session(request.user, workout_form)

            return JsonResponse({"success": True})
        return JsonResponse({"error": "Invalid Form"})


@login_required
def save_workout(request):
    if request.method == "POST":
        workout_form = WorkoutForm(request.POST)
        if workout_form.is_valid():
            save_custom_workout(request.user, workout_form)

            return JsonResponse({"success": True})
        return JsonResponse({"error": "Invalid Form"})


@login_required
def edit_workouts(request):
    exercises = list(
        Exercise.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )
    workouts = list(
        Workout.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )

    return render(
        request,
        "workout/edit_workouts.html",
        {"workouts": workouts, "exercises": exercises},
    )


@login_required
def exit_edit(request):
    exercises = list(
        Exercise.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )
    workouts = list(
        Workout.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )

    return render(
        request,
        "workout/workout_session.html",
        {"exercises": exercises, "workouts": workouts},
    )
from datetime import date
from matplotlib.ticker import MaxNLocator
from django.db.models import Max
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.relativedelta import relativedelta
from .models import *
from users.models import User
from .forms import (
    WorkoutForm,
    WorkoutSessionForm,
)
from .utils import *
from matplotlib import pyplot as plt
from io import BytesIO
import matplotlib

matplotlib.use("Agg")


# Create your views here.
class StatsView(LoginRequiredMixin, TemplateView):
    template_name = "workouts/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DEFAULT_USER = User.objects.get(username="default")
        exercises = list(Exercise.objects.filter(user=DEFAULT_USER))
        context["exercises"] = exercises
        return context

    def post(self, request, *args, **kwargs):
        months = int(request.POST["date_range"])
        stat = request.POST["stat"]
        user = request.user

        start_date = date.today() - relativedelta(months=months)
        end_date = date.today()

        if stat == "weightlifting":
            exercise_name = request.POST["exercise"]
            exercise = Exercise.objects.get(name=exercise_name, user=request.user)
            max_weight_info = (
                WorkoutSet.objects.filter(
                    exercise=exercise,
                    workout_log__date__range=[start_date, end_date],
                )
                .values("workout_log__date")
                .annotate(max_weight=Max("weight"))
                .order_by("workout_log__date")
            )

            dates = []
            weights = []
            for entry in max_weight_info:
                dates.append(entry["workout_log__date"].strftime("%#d/%#m"))
                weights.append(entry["max_weight"])
            # exercise_values = list(workout_sets.values_list("weight", flat=True))
            graph = self.plot_graph(exercise_name, weights, dates)
            return HttpResponse(graph, content_type="image/png")

        return render(request, "workouts/stats.html")

    def plot_graph(self, stat_name, values, dates):
        plt.close()
        plt.plot(dates, values)
        plt.xlabel("Date", color="#f5f5f5")
        plt.ylabel("Lbs.", color="#f5f5f5")
        plt.title(stat_name.capitalize(), color="#f5f5f5")

        plt.gcf().set_facecolor("#212121")
        plt.xticks(color="#f5f5f5")
        plt.yticks(color="#f5f5f5")

        ax = plt.gca()
        ax.set_facecolor("#212121")
        ax.xaxis.set_major_locator(MaxNLocator(12))
        ax.yaxis.set_major_locator(MaxNLocator(15))
        ax.tick_params(color="#f5f5f5")

        for spine in ax.spines.values():
            spine.set_edgecolor("#f5f5f5")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        return buffer.getvalue()


class SelectWorkoutView(LoginRequiredMixin, TemplateView):
    template_name = "workouts/workout.html"

    def get_context_data(self, **kwargs):
        workout_name = self.kwargs["workout_name"].replace("%20", " ")
        workout = Workout.get_workout(self.request.user, workout_name)
        context = super().get_context_data()
        context["workout"] = workout.configure_workout()
        return context


class WorkoutView(LoginRequiredMixin, View):

    def get(self, request):
        DEFAULT_USER = User.objects.get(username="default")
        exercises = list(
            Exercise.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
        )
        workouts = list(
            Workout.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
        )
        modules = ["workouts", "cardio", "log", "stats", "settings"]

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(
                request,
                "workouts/workout_session.html",
                {"modules": modules, "exercises": exercises, "workouts": workouts},
            )
        else:
            return render(
                request,
                "workouts/index.html",
                {"modules": modules, "exercises": exercises, "workouts": workouts},
            )


class AddExerciseView(LoginRequiredMixin, TemplateView):

    template_name = "workouts/exercise.html"

    def get_context_data(self, **kwargs):
        exercise_name = self.kwargs["exercise"].replace("%20", " ")
        sets = self.kwargs.get("sets")
        exercise = {"name": exercise_name}
        if sets is None:
            exercise["sets"] = [{"weight": "", "reps": ""}]
        else:
            exercise["sets"] = sets

        context = super().get_context_data(**kwargs)
        context["exercise"] = exercise
        return context


class AddSetView(LoginRequiredMixin, TemplateView):
    template_name = "workouts/set.html"


class SaveWorkoutSessionView(LoginRequiredMixin, FormView):
    form_class = WorkoutSessionForm

    def form_valid(self, form, *args, **kwargs):
        save_workout_session(self.request.user, form)
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        return JsonResponse({"error": "Invalid Form"})


class SaveWorkoutView(LoginRequiredMixin, FormView):
    form_class = WorkoutForm

    def form_valid(self, form, *args, **kwargs):
        save_custom_workout(self.request.user, form)
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        return JsonResponse({"error": "Invalid Form"})


@login_required
def edit_workouts(request):
    DEFAULT_USER = User.objects.get(username="default")
    exercises = list(
        Exercise.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )
    workouts = list(
        Workout.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )

    return render(
        request,
        "workouts/edit_workouts.html",
        {"workouts": workouts, "exercises": exercises},
    )


@login_required
def exit_edit(request):
    DEFAULT_USER = User.objects.get(username="default")
    exercises = list(
        Exercise.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )
    workouts = list(
        Workout.objects.filter(user=DEFAULT_USER).values_list("name", flat=True)
    )

    return render(
        request,
        "workouts/workout_session.html",
        {"exercises": exercises, "workouts": workouts},
    )

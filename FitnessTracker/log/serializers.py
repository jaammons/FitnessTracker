from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers
from datetime import timedelta, datetime, date
from workout.models import Exercise, Workout
from .models import CardioLog, WeightLog, WorkoutLog, WorkoutSet
from .validators import (
    validate_not_future_date,
    validate_not_more_than_5_years_ago,
    validate_duration_min,
    validate_duration_max,
)


class WorkoutSetSerializer(serializers.ModelSerializer):
    exercise = serializers.StringRelatedField()

    class Meta:
        model = WorkoutSet
        fields = ["workout_log", "exercise", "weight", "reps"]


class WorkoutLogSerializer(serializers.ModelSerializer):
    workout_sets = WorkoutSetSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        user = self.context["request"].user
        data["user"] = user
        data["workout"] = Workout.get_workout(
            user=user, workout_name=data["workout_name"]
        )
        data["total_time"] = timedelta(seconds=int(data.get("total_time", 0)))
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["workout_name"] = instance.workout.name
        exercises = {}

        for workout_set in data["workout_sets"]:
            exercise_name = workout_set["exercise"]
            if exercise_name not in exercises:
                exercises[exercise_name] = {"reps": [], "weights": []}

            exercises[exercise_name]["reps"].append(workout_set["reps"])
            exercises[exercise_name]["weights"].append(workout_set["weight"])

        data["exercises"] = exercises

        del data["workout_sets"]
        data["pk"] = instance.pk
        return data

    def create(self, validated_data):
        workout_log_data = {
            "workout": validated_data.get("workout"),
            "user": validated_data.get("user"),
            "date": validated_data.get("date"),
            "total_time": validated_data.get("total_time"),
        }
        with transaction.atomic():

            workout_log = WorkoutLog.objects.create(**workout_log_data)
            for exercise in validated_data.get("workout_exercises"):
                ((exercise_name, sets),) = exercise.items()
                exercise, _ = Exercise.objects.get_or_create(
                    user=validated_data["user"], name=exercise_name
                )
                for i in range(len(sets["reps"])):
                    workout_set = WorkoutSet.objects.create(
                        workout_log=workout_log,
                        exercise=exercise,
                        reps=sets["reps"][i],
                        weight=sets["weights"][i],
                    )
                    workout_set.full_clean()
            try:
                workout_log.full_clean()
            except ValidationError as e:
                raise serializers.ValidationError(e.message_dict)
            return workout_log

    class Meta:
        model = WorkoutLog
        fields = ["workout", "user", "date", "total_time", "workout_sets"]


class CardioLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardioLog
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_datetime(self, value):
        validate_not_future_date(value)
        validate_not_more_than_5_years_ago(value)
        return value

    def validate_duration(self, value):
        validate_duration_min(value)
        validate_duration_max(value)
        return value

    def validate_distance(self, value):
        validator_min = MinValueValidator(0)
        validator_max = MaxValueValidator(99.99)
        validator_min(value)
        validator_max(value)
        return value

    def to_internal_value(self, data):
        updated_data = {"datetime": data.get("datetime")}

        duration_hours = int(data.get("duration-hours", 0))
        duration_minutes = int(data.get("duration-minutes", 0))
        duration_seconds = int(data.get("duration-seconds", 0))
        updated_data["duration"] = timedelta(
            hours=duration_hours, minutes=duration_minutes, seconds=duration_seconds
        )

        distance_integer = data.get("distance-integer", 0)
        distance_decimal = data.get("distance-decimal", 0)
        updated_data["distance"] = float(f"{distance_integer}.{distance_decimal}")
        return super().to_internal_value(updated_data)


class WeightLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeightLog
        fields = "__all__"
        read_only_fields = ["user"]

    def to_internal_value(self, data):
        data_date = data.get("date")
        if not isinstance(data_date, datetime) and not isinstance(data_date, date):
            data["date"] = datetime.strptime(data_date, "%B %d, %Y").date()
        return data
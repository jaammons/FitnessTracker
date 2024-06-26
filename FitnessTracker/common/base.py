from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from common.permissions import IsOwner
from users.models import UserSettings, User
from django.shortcuts import render


class BaseOwnerViewSet(viewsets.ModelViewSet):
    """
    Abstract base viewset to restrict object operations to the owner of the object only.
    """

    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Return objects related to the logged-in user only.
        """
        return self.queryset.filter(
            Q(user=self.request.user) | Q(user=User.get_default_user())
        )

    def perform_create(self, serializer):
        """
        Automatically set the user of the created object to the logged-in user.
        """
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == User.get_default_user():
            raise PermissionDenied("Default workouts cannot be deleted.")
        return super().destroy(request, *args, **kwargs)


class BaseTemplateView(LoginRequiredMixin, TemplateView):
    """Abstract base template view that adds login required permissions, and user_settings to context"""

    template_name = None  # Template used for regular requests
    fetch_template_name = None  # Template used during a fetch request

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_settings"] = UserSettings.get_user_settings(self.request.user.id)

        if self.fetch_template_name:
            context["template_content"] = self.fetch_template_name

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if (
            self.fetch_template_name
            and request.headers.get("X-Requested-With") == "XMLHttpRequest"
        ):
            return render(request, self.fetch_template_name, context)
        return render(request, self.template_name, context)

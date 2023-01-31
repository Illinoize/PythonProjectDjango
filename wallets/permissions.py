"""Importing permissions"""
from rest_framework import permissions  # pylint: disable=E0401


class IsOwnerOrReadOnly(permissions.BasePermission):  # pylint: disable=R0903
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):  # pylint: disable=W0613
        """Getting permission for user"""
        return obj.owner == request.user

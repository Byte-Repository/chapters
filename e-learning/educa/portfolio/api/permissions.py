from rest_framework import permissions

class IsInstructorOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only instructors or admins to access all portfolio entries.
    """
    def has_permission(self, request, view):
        # Allow access if the user is an instructor or admin
        return request.user.is_staff

class IsStudent(permissions.BasePermission):
    """
    Custom permission to allow students to only view their own portfolio entries.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access to the portfolio entry only if it belongs to the logged-in user (student)
        return obj.student == request.user

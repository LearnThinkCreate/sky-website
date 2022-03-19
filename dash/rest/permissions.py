from rest_framework.permissions import BasePermission

class AttendanceManager(BasePermission):
    """
    User is a BB Attendance Manager
    """
    def has_permission(self, request, view):
        print(request.user.roles)
        print(request.user)
        perm = "Attendance Manager" in request.user.roles
        return perm

class Parent(BasePermission):
    """
    User is a TP Parent
    """
    def has_permission(self, request, view):
        perm = "Parent" in request.user.roles
        return perm

class Staff(BasePermission):
    """
    User is part of the TP Faculty or Staff
    """ 
    def has_permissions(self, request, view):
        perm = ["Teacher", "Non-Teaching Staff"] in request.user.roles
        return perm
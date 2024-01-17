from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Check if an user has 'manager' group
    """

    manager_methods = ('POST', 'PUT', 'PATCH', 'DELETE')

    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            return False

        if request.method == 'GET':
            return True
        
        if request.method in self.manager_methods:
            if request.method == 'PUT' or request.method == 'PATCH':
                if request.data.get('status', None) and request.user.groups.filter(name='manager').exists():
                    return True

        return False


class IsAssistant(permissions.BasePermission):
    """
    Check if an user has 'assistant' group
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="assistant").exists()

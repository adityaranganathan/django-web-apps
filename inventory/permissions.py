from rest_framework import permissions

class IsPostRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if request.method in ['POST']:
            return True
        return False
        
class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            return True
        return False
        
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            return True
        return False

class IsCorrectUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return request.user == obj.user
        if hasattr(obj, "retailer"):
            return request.user == obj.retailer.user
        
class IsProductRetailerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow retailers of a product to edit it.
    """

    def has_object_permission(self, request, view, product):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return product.retailer.user == request.user
        
        
class IsRetailerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow retailers edit their own profile.
    """

    def has_object_permission(self, request, view, retailer):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return retailer.user == request.user
        
class IsCustomUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow retailers edit their own profile.
    """

    def has_object_permission(self, request, view, user):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return user == request.user
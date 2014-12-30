from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''
    This is for views that need tighter permissions than the ones with
    IsAdminOrInstructor. For views like add/create instructor, or delete
    a course that is not yours.
    '''

    def has_object_permission(self, request, view, obj):
        # based on view on django-rest site, slightly modified
        # Read permissions are allowed for all instructors,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        # of the object or admins.
        return (obj.professor == request.user or
                request.user.profile.profile_type == 'AD')

from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsObjectOwner(IsAuthenticated):

	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		if hasattr(obj, 'created_by'):
			return obj.created_by == request.user
		return False
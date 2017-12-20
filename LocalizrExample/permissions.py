from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedOrOptionsRequest(IsAuthenticated):
  """
  If it is authenticated or options request.
  """

  def has_permission(self, request, view):
    if request.method == 'OPTIONS':
      return True
    return super(IsAuthenticatedOrOptionsRequest, self).has_permission(request, view)
from django.http import JsonResponse
from django.conf import settings

class AjaxLoginRequiredMiddleware:
    """
    Middleware to ensure that AJAX requests are properly redirected to the login page
    when the user is not authenticated.
    It ensures that unauthenticated AJAX requests receive a proper JSON response 
    instead of a standard HTTP redirect, which doesn't work well with AJAX.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        '''
        In order to check if a request is an AJAX request, the "HTTP_X_REQUESTED_WITH" header
        has to be inspected. It should be set to "XMLHttpRequest" for AJAX requests.
        '''
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and not request.user.is_authenticated:
            return JsonResponse({'login_url': settings.LOGIN_URL}, status=403)
        response = self.get_response(request)
        return response

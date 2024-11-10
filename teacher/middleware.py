from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class PreventBackHistoryMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        """
        Add headers to prevent browser caching and enable no-store behavior,
        similar to Laravel's middleware.
        """
        response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 'Sat, 26 Jul 1997 05:00:00 GMT'  # Expire in the past

        return response
    
class AdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Restrict non-admin users from accessing 'teacher' pages
        if request.user.is_authenticated and not request.user.is_staff and request.path.startswith('/teacher'):
            return redirect('landing')  # Redirect non-admin users to user dashboard

        # Restrict admin users from accessing 'login_page' and 'signup_page' URLs
        if request.user.is_authenticated and request.user.is_staff and (request.path == '/login_page/' or request.path == '/signup_page/'):
            return redirect('teacher_dashboard')  # Redirect admin users to dashboard or another page

        return self.get_response(request)


class RedirectUnauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the URLs that require authentication
        protected_urls = [
            reverse('teacher_dashboard'),
        ]

        # Check if the user is not authenticated and trying to access protected URLs
        if not request.user.is_authenticated and request.path in protected_urls:
            return redirect('login_page')  # Redirect unauthenticated users to the main page

        return self.get_response(request)

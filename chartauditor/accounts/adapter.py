from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse_lazy


class MyAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):
        return reverse_lazy('profile')

    def get_login_redirect_url(self, request):
        if request.user.is_profile:
            return reverse_lazy('chart_audit')
        return reverse_lazy('profile')

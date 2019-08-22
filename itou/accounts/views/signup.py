"""
Handle multiple user types sign up with django-allauth.
"""
from allauth.account.views import SignupView

from django.db import transaction

from itou.accounts import forms


class PrescriberSignupView(SignupView):

    form_class = forms.PrescriberSignupForm
    template_name = 'account_itou/signup_prescriber.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Enforce atomicity."""
        return super().post(request, *args, **kwargs)


class SiaeSignupView(SignupView):

    form_class = forms.SiaeSignupForm
    template_name = 'account_itou/signup_siae.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Enforce atomicity."""
        return super().post(request, *args, **kwargs)


class JobSeekerSignupView(SignupView):

    form_class = forms.JobSeekerSignupForm
    template_name = 'account_itou/signup_job_seeker.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Enforce atomicity."""
        return super().post(request, *args, **kwargs)

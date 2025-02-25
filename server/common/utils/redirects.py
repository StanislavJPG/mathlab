from django.http import HttpResponse
from django.shortcuts import reverse


def theorist_email_verification_redirect_view(request, pk, full_name_slug):
    response = HttpResponse()
    response['HX-Redirect'] = reverse('forum:theorist_profile:base-page', args=[pk, full_name_slug])
    return response

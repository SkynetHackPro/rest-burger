import json

from django.http import HttpResponse


def authorisation(request):
    print(request.user)
    return HttpResponse(123)

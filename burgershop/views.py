import json

from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden

from burgershop.models import User


def authorisation(request):
    json_data = json.loads(request.body.decode('utf-8'))
    try:
        login = json_data['login']
        password = json_data['password']
    except KeyError:
        return HttpResponseBadRequest()

    try:
        user = User.object.get(username=login)
    except User.DoesNotExist:
        return HttpResponseForbidden()

    if check_password(password, user.password):
        token = user.authenticate_by_token()
    else:
        return HttpResponseForbidden()
    return HttpResponse(json.dumps({
        'token': token
    }))


import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods

from burgershop.models import User, MenuCategory


@require_http_methods(["POST"])
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
    return JsonResponse({
        'token': token
    })


def get_menu(request):
    serialised = MenuCategory.objects.get_serialised_with_items()
    return JsonResponse(serialised)

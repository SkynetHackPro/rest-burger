import json

from django.contrib.auth.hashers import check_password
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods

from burgershop.models import User, MenuCategory, MenuItem, Order
from burgershop.utils import custom_login_required


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


@custom_login_required
def get_menu(request):
    serialised = MenuCategory.objects.get_serialised_with_items()
    return JsonResponse(serialised)


@custom_login_required
@require_http_methods(["POST"])
def create_order(request):
    order_items_pks = json.loads(request.body.decode('utf-8'))['items']
    order_items_count = {i: order_items_pks.count(i) for i in order_items_pks}
    order_items = MenuItem.objects.filter(pk__in=order_items_pks)
    order = Order(
        dealer=request.user
    )
    order.save()
    for item in order_items:
        count = order_items_count[item.pk]
        for i in range(0, count):
            order.order_items.create(
                item=item,
                price=item.price
            )
    return JsonResponse({'status': 'ok'})

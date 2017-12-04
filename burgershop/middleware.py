import json

from django.utils.deprecation import MiddlewareMixin

from burgershop.models import AuthToken


class TokenAuthorizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated():
            token = None
            if request.method == 'POST':
                try:
                    json_data = json.loads(request.body.decode("utf-8"))
                    if 'token' in json_data:
                        token = json_data['token']
                except json.JSONDecodeError:
                    pass
            elif request.method == 'GET':
                if 'token' in request.GET:
                    token = request.GET['token']

            try:
                request.user = AuthToken.objects.get(token=token, user__is_dealer=True).user
            except AuthToken.DoesNotExist:
                pass

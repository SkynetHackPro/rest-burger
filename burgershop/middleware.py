import json

from django.utils.deprecation import MiddlewareMixin

from burgershop.models import AuthToken


class TokenAuthorizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated():
            if request.method == 'POST':
                json_data = json.loads(request.body.decode("utf-8"))
                if 'token' in json_data:
                    token = json_data['token']
                    try:
                        request.user = AuthToken.objects.get(token=token).user
                    except AuthToken.DoesNotExist:
                        pass

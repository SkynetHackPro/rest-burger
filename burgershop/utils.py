from django.http import HttpResponseForbidden


def custom_login_required(view):
    def auth_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return view(request, *args, **kwargs)
    return auth_view

from django.conf.urls import url
from django.contrib import admin

from burgershop.views import authorisation, get_menu, create_order

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth', authorisation),
    url(r'^get_menu', get_menu),
    url(r'^create_order', create_order)
]

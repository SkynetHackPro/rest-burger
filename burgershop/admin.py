from adminsortable.admin import SortableAdmin
from django import forms
from django.contrib import admin

from django.apps import apps
from mptt.admin import DraggableMPTTAdmin

from burgershop.models import User, MenuCategory, MenuItem, Order, OrderItem, BurgerShop, City

app = apps.get_app_config('burgershop')


class UserForm(forms.ModelForm):
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'is_staff', 'is_superuser', 'is_dealer')
        model = User

    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(admin.ModelAdmin):
    form = UserForm


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 50
    fields = ('name', 'items')
    filter_horizontal = ('items',)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item', 'price')
    can_delete = False

    def has_add_permission(self, request):
        return False


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemsInline,)
    readonly_fields = ('dealer',)


class BurgerShopAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, CustomUserAdmin)
admin.site.register(MenuCategory, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BurgerShop, BurgerShopAdmin)
admin.site.register(City, CityAdmin)

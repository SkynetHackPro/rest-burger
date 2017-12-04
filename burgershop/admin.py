from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from mptt.admin import DraggableMPTTAdmin

from burgershop.models import User, MenuCategory, MenuItem, Order, OrderItem, BurgerShop, City

admin.site.unregister(Group)


class UserForm(forms.ModelForm):
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False)

    class Meta:
        fields = ('username', 'is_staff', 'is_dealer', 'burgershop')
        model = User

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if not cleaned_data['burgershop'] and cleaned_data['is_dealer']:
            self.add_error('burgershop', 'Нужно указать место работы оператора')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user.is_superuser = self.cleaned_data['is_staff']
        if self.cleaned_data["new_password"]:
            user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('burgershop', 'is_dealer',)
    list_display = ('username', 'burgershop', 'is_dealer',)
    form = UserForm


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 50
    fields = ('name', 'items',)
    filter_horizontal = ('items',)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item', 'price',)
    can_delete = False

    def has_add_permission(self, request):
        return False


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemsInline,)
    list_display = ('__str__', 'dealer', 'order_sum', 'status', 'time',)
    readonly_fields = ('dealer', 'order_sum', 'order_burgershop', 'time',)
    list_filter = ('dealer', 'dealer__burgershop', 'dealer__burgershop__city',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(OrderAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class BurgerShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(MenuCategory, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BurgerShop, BurgerShopAdmin)
admin.site.register(City)

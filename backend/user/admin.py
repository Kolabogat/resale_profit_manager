from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import UserSettings, UserProfile


@admin.register(UserSettings)
class UserSettingsAdmin(ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('id', 'user', 'paginate_by', 'currency', 'display_symbol', 'delete_confirmation',)
    list_display_links = ('id', 'user',)
    search_fields = ('id', 'user',)
    fields = ('id', 'user', 'paginate_by', 'currency', 'display_symbol', 'delete_confirmation',)
    readonly_fields = ('id', 'user')
    list_filter = ('display_symbol', 'paginate_by', 'delete_confirmation')


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('id', 'user', 'all_time_profit', 'tickets_quantity', 'highest_profit', 'highest_loss',)
    list_display_links = ('id', 'user',)
    search_fields = ('id', 'user',)
    fields = ('id', 'user', 'all_time_profit', 'tickets_quantity', 'highest_profit', 'highest_loss',)
    readonly_fields = ('id', 'user')


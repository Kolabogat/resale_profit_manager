from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Category, Ticket

ADMIN_ORDERING = {
    'Tickets': 1,
    'Categories': 2,

    'Users': 1,
    'Groups': 2,

    'Additional User Settings': 1,
}


def get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    # Retrieve the original list
    app_dict = self._build_app_dict(request, app_label)
    # Sort the apps alphabetically.
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(key=lambda x: ADMIN_ORDERING[x['name']])

    return app_list


admin.AdminSite.get_app_list = get_app_list


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'user', 'bought', 'sold', 'profit', 'category', 'created_at', 'closed_at', 'closed')
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'user', 'category')
    fieldsets = (
        ('Ticket', {
            'fields': (
                ('title', 'category'),
                ('user', 'deleted', 'closed'),
                'bought',
                'sold',
                'profit',
                ('created_at', 'closed_at'),
            ),
        }),
    )
    readonly_fields = ('created_at', 'closed_at')
    list_filter = ('closed', 'closed')


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('id', 'title')
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title',)
    fieldsets = (
            ('Category', {
                'fields': (
                    ('id', 'title'),
                ),
            }),
        )
    readonly_fields = ('id', )


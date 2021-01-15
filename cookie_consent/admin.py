from django.contrib import admin
from .models import (
    Cookie,
    CookieCategory,
    CookieGroup,
)


class CookieCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CookieAdmin(admin.ModelAdmin):
    list_display = ('varname', 'name', 'cookiegroup', 'path', 'domain',
                    'get_version')
    search_fields = ('name', 'domain', 'cookiegroup__varname',
                     'cookiegroup__name')
    readonly_fields = ('varname',)
    list_filter = ('cookiegroup',)


class CookieGroupAdmin(admin.ModelAdmin):
    list_display = ('varname', 'name', 'is_required', 'is_deletable',
                    'get_version')
    search_fields = ('varname', 'name',)
    list_filter = ('is_required', 'is_deletable',)


admin.site.register(Cookie, CookieAdmin)
admin.site.register(CookieGroup, CookieGroupAdmin)
admin.site.register(CookieCategory, CookieCategoryAdmin)

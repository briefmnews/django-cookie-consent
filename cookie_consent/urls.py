# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    CookieGroupFormView,
    CookieGroupAcceptView,
    CookieGroupDeclineView,
)

urlpatterns = [
    re_path(r'^accept/$',
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name='cookie_consent_accept_all'),
    re_path(r'^accept/(?P<varname>.*)/$',
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name='cookie_consent_accept'),
    re_path(r'^decline/(?P<varname>.*)/$',
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name='cookie_consent_decline'),
    re_path(r'^decline/$',
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name='cookie_consent_decline_all'),
    re_path(r'^$',
        CookieGroupFormView.as_view(),
        name='cookie_consent_cookie_group_list'),
]

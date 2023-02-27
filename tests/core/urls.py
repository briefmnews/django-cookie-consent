# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import re_path

from .views import (
    TestPageView,
)

urlpatterns = [
    re_path(r'^$',
        TestPageView.as_view(),
        name='test_page'),
]

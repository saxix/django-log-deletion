from __future__ import absolute_import
from django.contrib import admin
from django.conf.urls import include, url

import log_deletion.urls

admin.autodiscover()
urlpatterns = (
    url(r's/', include(log_deletion.urls)),
    url(r'admin/', include(admin.site.urls)),
)

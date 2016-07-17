from django.conf.urls import include, url
from django.contrib import admin

from sms.views import MainView

urlpatterns = [
    # Examples
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', MainView.as_view(), name='home'),
    url(r'^send/$', MainView.as_view(), name='send'),
]

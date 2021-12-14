from django.conf.urls import include, url

from AppBase.views import appBaseExceptionView

urlpatterns = [
    url(r'^exception/(?P<context>[-\w]+)$', appBaseExceptionView, {'template_name': 'appbase/apps_exception.html'}, name="apps_exception"),
]

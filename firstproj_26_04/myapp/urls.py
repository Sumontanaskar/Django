from django.conf.urls import url
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # /myapp/
    url(r'^$', views.index, name='index'),
    # /myapp/id/
    url(r'^(?P<host_id>[0-9]+)/$', views.detail, name='detail'),
    #/myapp/host?=vpc-prod-vertex08-usw/
    url(r'^host_details$', views.host_details, name='host_details'),
    # /myapp/result
    url(r'^results/$', views.results, name='result'),
    #/myapp/list
    url(r'^upload/$', views.upload, name='upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
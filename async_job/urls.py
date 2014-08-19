from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from async_job import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'async_job.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^progress/(?P<job_id>\d+)/$', views.progress),
    url(r'^progress/(?P<job_id>\d+)/json/$', views.progress_json),
    url(r'^upload/$', views.file_upload),
    url(r'^success/(?P<fileupload_id>\d+)/$', views.success),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

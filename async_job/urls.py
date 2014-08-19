from django.conf.urls import patterns, include, url

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
)

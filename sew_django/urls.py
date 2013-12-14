from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sew_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:],  # cut away leading slash
         'django.views.static.serve', {'document_root': settings.STATIC_ROOT,
                                       'show_indexes': True}),
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],  # cut away leading slash
         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
                                       'show_indexes': True}),
)

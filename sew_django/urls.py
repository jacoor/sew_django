from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('sew_django.profiles.urls')),
    url(r"^admin/", include(admin.site.urls)),
    (r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:],  # cut away leading slash
         'django.views.static.serve', {'document_root': settings.STATIC_ROOT,
                                       'show_indexes': True}),
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],  # cut away leading slash
         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
                                       'show_indexes': True}),

    #(r'^grappelli/', include('grappelli.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sew_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r"^$", TemplateView.as_view(template_name="index.html"), name="index"),
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

from django.conf.urls import patterns, include, url
from bracketapp.views import register, bracket_create
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'brackets.views.home', name='home'),
    # url(r'^brackets/', include('brackets.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^newbracket/$',bracket_create),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^newuser/$',register),
     url(r'^welcome/$',TemplateView.as_view(
         template_name='base.html'))
)

from django.conf.urls import patterns, include, url
from bracketapp.views import register, bracket_create
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'brackets.views.home', name='home'),
    # url(r'^brackets/', include('brackets.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^$', RedirectView.as_view(url="/home")),
     url(r'^newbracket/$',bracket_create),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^register/$',register),
     url(r'^home/$',TemplateView.as_view(
         template_name='base.html')),
     url(r'^login/$', login),
     url(r'^logout/$', logout, {'next_page': '/'}),
     url(r'^about/$',TemplateView.as_view(
         template_name='about.html')),
)

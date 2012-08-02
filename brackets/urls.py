from django.conf.urls import patterns, include, url
from bracketapp.views import register,BracketCreateView, BracketModify, BracketDetailView, UnresolvedCompetitionListView
from django.views.generic import (TemplateView, RedirectView, CreateView,
    ListView, DetailView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User
from bracketapp.models import Bracket
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
     url(r'^create/$', BracketCreateView.as_view(template_name='create.html',success_url="/success/")),
     url(r'^success/$', TemplateView.as_view(
         template_name='success.html')),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^register/$',register),
     url(r'^bracket/(?P<pk>\d+)/$',BracketDetailView.as_view(model=Bracket, template_name='bracket_detail.html')),
     url(r'^bracket/(?P<pk>\d+)/contest_resolve/$',UnresolvedCompetitionListView.as_view(template_name='competition_resolver.html')),
     url(r'^home/$',TemplateView.as_view(
         template_name='base.html')),
     url(r'^login/$', login),
     url(r'^logout/$', logout, {'next_page': '/'}),
     url(r'^about/$',TemplateView.as_view(
         template_name='about.html')),
     url(r'^list/$', ListView.as_view(model=Bracket, queryset=Bracket.objects.order_by('title'),template_name='list.html')),
     url(r'^account/$', TemplateView.as_view(template_name='account.html')),
     url(r'^modify/(?P<pk>\d+)/$',BracketModify.as_view(),name="modify_bracket"),
)

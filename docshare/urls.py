from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
import settings
import users.views
import documents.views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'css/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.TEMPLATE_DIRS[0]+'/css'}),
    url(r'js/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.TEMPLATE_DIRS[0]+'/js'}),
    url(r'images/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.TEMPLATE_DIRS[0]+'/images'}),
    url(r'fonts/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.TEMPLATE_DIRS[0]+'/fonts'}),
    # Examples:
    # url(r'^$', 'docshare.views.home', name='home'),
    # url(r'^docshare/', include('docshare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$',users.views.login),
    url(r'^register.html', users.views.register),
    url(r'^logout/', users.views.logout),
    url(r'^admin/logout/', users.views.logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^loginChecker',users.views.user_login_checker),
    url(r'^registerChecker',users.views.user_register_checker),
    url(r'^homepage/',users.views.homepage),
    url('^upload/$', documents.views.upload_file),
    url(r'^render/(\d+)/$', documents.views.render_pdf),
    url(r'^docs/(?P<doc_id>\d+)/$', documents.views.serve_pdf),
)

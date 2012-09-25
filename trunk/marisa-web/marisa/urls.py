from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'search.views.index', name='home'),
    #url(r'^wly_management/', include('wly_management.foo.urls')),
    url(r'^auth/logout', 'auth.views.logout_view', name='home'),
    
    url(r'^unavailable', 'overview.views.unavailable', name='home'),    
    url(r'^search$', 'search.views.index', name='home'),    
    

    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

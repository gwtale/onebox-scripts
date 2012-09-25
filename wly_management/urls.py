from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'overview.views.index', name='home'),
    #url(r'^wly_management/', include('wly_management.foo.urls')),
    url(r'^auth/logout', 'auth.views.logout_view', name='home'),
    
    url(r'^clientinfo/$', 'clientinfo.views.index', name='home'),
    url(r'^clientinfo/setup_amounts', 'clientinfo.views.setup_amounts', name='home'), 
    url(r'^clientinfo/get_setup_amounts', 'clientinfo.views.get_setup_amounts', name='home'),    

    url(r'^userinfo/$', 'userinfo.views.index', name='home'),
    url(r'^userinfo/user_location', 'userinfo.views.user_location', name='home'),    
    url(r'^userinfo/paidinfo', 'userinfo.views.paidinfo', name='home'),    
    url(r'^userinfo/use_time', 'userinfo.views.use_time', name='home'),    
    url(r'^userinfo/online_users', 'userinfo.views.online_users', name='home'), 
    url(r'^userinfo/get_online_users', 'userinfo.views.get_online_users', name='home'),    
    url(r'^userinfo/user_modify', 'userinfo.views.user_modify', name='home'),    
    url(r'^userinfo/cash_modify', 'userinfo.views.cash_modify', name='home'),    
    url(r'^userinfo/push_cash_modify', 'userinfo.views.push_cash_modify', name='home'),    
    url(r'^userinfo/get_user_info', 'userinfo.views.get_user_info', name='home'),    
    url(r'^userinfo/submit_modify_user', 'userinfo.views.submit_modify_user', name='home'),    
    url(r'^userinfo/user_list', 'userinfo.views.user_list', name='home'),    
    
    
    url(r'^unavailable', 'overview.views.unavailable', name='home'),    

    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

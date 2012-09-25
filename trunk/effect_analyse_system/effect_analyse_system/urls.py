from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'overview.views.index', name='home'),
    url(r'^overview/get_click_and_search_amounts$', 'overview.views.get_click_and_search_amounts', name='get_click_and_search_amounts'),

    url(r'^overview/get_click_rate$', 'overview.views.get_click_rate', name='get_click_rate'),
    url(r'^overview/click_rate$', 'overview.views.click_rate', name='click_rate'),

    url(r'^overview/get_first_click_time$', 'overview.views.get_first_click_time', name='get_first_click_time'),
    url(r'^overview/first_click_time$', 'overview.views.first_click_time', name='first_click_time'),

    url(r'^overview/get_non_click_rate$', 'overview.views.get_non_click_rate', name='get_non_click_rate'),
    url(r'^overview/non_click_rate$', 'overview.views.non_click_rate', name='non_click_rate'),

    url(r'^overview/get_page_change_rate$', 'overview.views.get_page_change_rate', name='get_non_click_rate'),
    url(r'^overview/page_change_rate$', 'overview.views.page_change_rate', name='non_click_rate'),


    url(r'^overview/get_page_change_insearch_rate$', 'overview.views.get_page_change_insearch_rate', name='get_page_change_insearch_rate'),
    url(r'^overview/page_change_insearch_rate$', 'overview.views.page_change_insearch_rate', name='page_change_insearch_rate'),
    url(r'^overview/get_top3_click_rate$', 'overview.views.get_top3_click_rate', name='get_top3_click_rate'),
    url(r'^overview/top3_click_rate$', 'overview.views.top3_click_rate', name='top3_click_rate'),

    url(r'^overview/get_pos_click_rate$', 'overview.views.get_pos_click_rate', name='get_pos_click_rate'),
    url(r'^overview/pos_click_rate$', 'overview.views.pos_click_rate', name='pos_click_rate'),

    url(r'^overview/get_query_change_rate$', 'overview.views.get_query_change_rate', name='get_query_change_rate'),
    url(r'^overview/query_change_rate$', 'overview.views.query_change_rate', name='query_change_rate'),

    url(r'^overview/page$', 'overview.views.page', name='page'),
    url(r'^overview/get_page$', 'overview.views.get_page', name='get_page'),


    #url(r'^wly_management/', include('wly_management.foo.urls')),
    
    url(r'^unavailable', 'overview.views.unavailable', name='home'),    
    url(r'^external$', 'external.views.index', name='external'),    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

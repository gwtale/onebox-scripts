import os
from django.shortcuts import render_to_response
from django.db.models import Sum, Avg
from chartit import PivotChart, PivotDataPool
from demoproject.utils.decorators import add_source_code_and_doc
from models import SalesHistory


@add_source_code_and_doc
def simplepivot(request, title, code, doc, sidebar_items):
    """
    A simple pivot chart.
    
    Points to notice:
    
    - You can use the default django convention of double underscore (__) to 
      *follow* to the fields in different models.
    """
    #start_code
    ds = PivotDataPool(
          series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': 'bookstore__city__city'},
            'terms': {
              'tot_sales':Sum('sale_qty')}}])
    
    pivcht = PivotChart(
              datasource = ds, 
              series_options = [
                {'options': {
                   'type': 'column'},
                 'terms': ['tot_sales']}])
    #end_code
    return render_to_response('chart_code.html', {'chart_list': pivcht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})
    
@add_source_code_and_doc
def pivot_with_legend(request, title, code, doc, sidebar_items):
    """
    Pivot Chart with legend by field. This pivot chart plots total sale 
    quantity of books in each city legended by the book genre name.
    """
    #start_code
    ds = PivotDataPool(
          series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': 'bookstore__city__city',
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales':Sum('sale_qty')}}])
    
    pivcht = PivotChart(
              datasource = ds, 
              series_options = [
                {'options': {
                   'type': 'column',
                   'stacking': True, 
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    #end_code
    return render_to_response('chart_code.html', {'chart_list': pivcht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})

@add_source_code_and_doc
def pivot_multi_category(request, title, code, doc, sidebar_items):
    """
    Pivot Chart with multiple categories. In this chart the total sale 
    quantity is plotted with respect to state and city.
    
    Points to note:
    
    - You can add any number of categories and legend_by entries in a list. 
    - **Order matters**! Retrieving state and then city may yield different 
      results compared to retrieving city and state depending on what you 
      are trying to plot.
    """
    #start_code
    ds = PivotDataPool(
          series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales':Sum('sale_qty')}}])
    
    pivcht = PivotChart(
              datasource = ds, 
              series_options = [
                {'options': {
                   'type': 'column',
                   'stacking': True, 
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    #end_code
    return render_to_response('chart_code.html', {'chart_list': pivcht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})

@add_source_code_and_doc
def pivot_with_top_n_per_cat(request, title, code, doc, sidebar_items):
    """
    Pivot Chart each category limited to a select top items.
    
    Points to note:
    
    - These charts are helpful when there are too many items in each category
      and we only want to focus on the top few items in each category.
    """
    #start_code
    ds = PivotDataPool(
          series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name',
              'top_n_per_cat': 2},
            'terms': {
              'tot_sales':Sum('sale_qty')}}])
    
    pivcht = PivotChart(
              datasource = ds, 
              series_options = [
                {'options': {
                   'type': 'column',
                   'stacking': True, 
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    #end_code
    return render_to_response('chart_code.html', {'chart_list': pivcht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_top_n(request, title, code, doc, sidebar_items):
    """
    Pivot Chart limited to top few items. In this chart the sales quanity is 
    plotted w.r.t state/city but the chart is limited to only top 5 cities 
    witht the highest sales.
    
    Points to note:
    
    - These charts are helpful in cases where there is a long *tail* and we 
      only are interested in the top few items.
    - ``top_n_term`` is always required. If there are multiple items, it will 
      elimnate confusion regarding what the term the chart needs to be 
      limited by.
    """
    #start_code
    ds = PivotDataPool(
          series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales':Sum('sale_qty')}}],
          top_n = 5,
          top_n_term = 'tot_sales')
    
    pivcht = PivotChart(
              datasource = ds, 
              series_options = [
                {'options': {
                   'type': 'column',
                   'stacking': True, 
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    #end_code
    return render_to_response('chart_code.html', {'chart_list': pivcht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})

@add_source_code_and_doc
def pivot_pareto(request, title, code, doc, sidebar_items):
    """
    Pivot Chart plotted as a `pareto chart 
    <http://en.wikipedia.org/wiki/Pareto_chart>`_ w.r.t the total sales 
    quantity.
    """
    #start_code
    ds = PivotDataPool(
          series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales':Sum('sale_qty')}}],
          top_n = 5,
          top_n_term = 'tot_sales',
          pareto_term = 'tot_sales')
    
    pivcht = PivotChart(
              datasource = ds, 
              series_options = [
                {'options': {
                   'type': 'column',
                   'stacking': True, 
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    #end_code
    return render_to_response('chart_code.html', {'chart_list': pivcht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})

@add_source_code_and_doc
def pivot_multi_axes(request, title, code, doc, sidebar_items):
    """
    Pivot Chart with multiple terms on multiple axes.
    
    Points to note:
    
    - Note that the term ``avg-price`` is passed as a dict (instead of as a 
      django aggregate to allow us to override the default ``legend_by`` 
      option. When passed as a dict, the aggregate function needs to be passed
      to the ``func`` key. 
    - Alternatively this could be written as ::
    
        series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales':Sum('sale_qty')}},
              
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city']},
            'terms': {
              'avg_price':Avg('price')}}
              ]
              
      but the one used in the code is more succint and has less duplication.
    """
    #start_code
    ds = PivotDataPool(
          series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales':Sum('sale_qty'),
              'avg_price':{
                'func': Avg('price'),
                'legend_by': None}}}],
          top_n = 5,
          top_n_term = 'tot_sales',
          pareto_term = 'tot_sales')
    
    pivcht = PivotChart(
              datasource = ds, 
              series_options = [
                {'options': {
                   'type': 'column',
                   'stacking': True},
                 'terms': [
                    'tot_sales',
                    {'avg_price': {
                        'type': 'line',
                        'yAxis': 1}}]}],
              chart_options = {
                'yAxis': [{}, {'opposite': True}]})
    #end_code
    return render_to_response('chart_code.html', {'chart_list': pivcht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})

@add_source_code_and_doc
def pivot_mapf(request, title, code, doc, sidebar_items):
    """
    Pivot Chart with ``sortf_mapf_mts`` defined to map custom names for x-axis
    and to customize the x-axis sorting. In this chart we would like to plot 
    region:city instead of state:city. However region is not available in the 
    database. So custom mapf function comes to the rescue.
    
    Points to note:
    
    - Note that ``mapf`` receives a tuple and returns a tuple. This is true 
      even when ``categories`` is a single element.
    - ``mts=True`` causes the elements to be mapped and then sorted. So all the 
      N region cities are on the left and the S region cities are on the right
      hand side of the plot. 
    """
    #start_code
    def region_state(x):
        region = {'CA': 'S', 'MA': 'N', 'TX': 'S', 'NY': 'N'}
        return (region[x[0]], x[1])
    
    ds = PivotDataPool(
          series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales':Sum('sale_qty')}}],
          sortf_mapf_mts = (None, region_state, True))
    
    pivcht = PivotChart(
              datasource = ds, 
              series_options = [
                {'options': {
                   'type': 'column',
                   'stacking': True},
                 'terms': [
                    'tot_sales']}])
    #end_code
    return render_to_response('chart_code.html', {'chart_list': pivcht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})

@add_source_code_and_doc
def model_details(request, title, code, doc, sidebar_items):
    """
    All the charts in this section are based on the following Models. The raw 
    data is available as a ``SQLite3`` database file  
    `here <../../static/db/chartitdemodb>`_. You can download the file and use 
    `SQLiteBrowser <http://sqlitebrowser.sourceforge.net/>`_ 
    to look at the raw data. 
    """
    fname = os.path.join(os.path.split(os.path.abspath(__file__))[0], 
                         'models.py')
    
    with open(fname) as f:
        code = ''.join(f.readlines())
    
    return render_to_response('model_details.html', 
                              {'code': code,
                               'title': title,
                               'doc': doc,
                               'sidebar_items': sidebar_items})
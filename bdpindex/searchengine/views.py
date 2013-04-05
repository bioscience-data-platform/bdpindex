import logging
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from bdpindex.searchengine import search

from bdpindex.searchengine.form import SearchForm
logger = logging.getLogger(__name__)

def index(request):
    #form = SearchForm()
    form = SearchForm(request.POST)
    print "index function"

    if form.is_valid():
        post_request_values = form.cleaned_data
        print post_request_values
        query = post_request_values['query_field']
        search_result = '\n'.join(search.search(query))
        print '%s ' % search_result
        return render(request, 'displayresult.html',
                  {'search_phrase': query,
                   'search_result': search.search(query)})

    else:
        search.index_data('cheers')
        return render(request, 'index.html', {
            'form': form})



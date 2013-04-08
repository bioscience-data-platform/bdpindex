import logging
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from bdpindex.searchengine import search

from bdpindex.searchengine.form import SearchForm
logger = logging.getLogger(__name__)

def index(request):
    #form = SearchForm()
    print "top index function"
    form = SearchForm(request.POST)
    print "index function"

    if form.is_valid():
        post_request_values = form.cleaned_data
        print post_request_values
        search_phrase = post_request_values['query_field']
        search_result = (search.search(search_phrase,
                                       index=False))
        print '%s ' % search_result
        repos = search.pull_data('http://115.146.85.142/')
    else:
        print 'not valid form'
        return render(request, 'index.html',
                      {'form': form,
                       })

    return render(request, 'displayresult.html',
                  {'search_phrase': search_phrase,
                   'search_result': search_result,
                   'repos': repos})



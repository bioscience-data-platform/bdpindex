import logging
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

from bdpindex.searchengine.form import SearchForm
logger = logging.getLogger(__name__)


def index(request):
    form = SearchForm()
    return render(request, 'index.html', {
        'form': form})




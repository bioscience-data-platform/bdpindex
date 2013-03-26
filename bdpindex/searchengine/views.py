# Create your views here.

import logging
from django.http import HttpResponse
from django.template import Context, RequestContext, loader
from django.conf import settings

logger = logging.getLogger(__name__)


def index(request):
    print "language code", settings.LANGUAGE_CODE
    template = loader.get_template('index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


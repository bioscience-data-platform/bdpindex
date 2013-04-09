from django.core.management.base import BaseCommand, CommandError
from bdpindex.searchengine import search

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<source_url source_url ...>'
    help = 'Indexes public MyTardis data'

    def handle(self, *args, **options):
        if 'all' in args:
            logger.debug('all')
            self.get_all_source_url(args)
            logger.debug('all=%s' % args)

        for source_url in args:
            records = search.pull_data('http://' + source_url)
            search.index_data(records)
            print "done"


    def get_all_source_url(self, args):
        pass

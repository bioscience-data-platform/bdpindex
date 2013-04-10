from django.core.management.base import BaseCommand, CommandError
from bdpindex.searchengine import search
from bdpindex.searchengine import models

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<source_url source_url ...>'
    help = 'Indexes public MyTardis data'

    def handle(self, *args, **options):
        mytardis_urls = []
        if 'all' in args:
            mytardis_urls = self.get_all_source_url()
        else:
            for arg in args:
                mytardis_urls.append('http://' + str(arg))
        logger.debug('mytardis_urls=%s' % mytardis_urls)
        for url in mytardis_urls:
            records = search.pull_data(str(url))
            search.index_data(records)
        logger.debug('Indexing completed')

    def get_all_source_url(self):
        mytaris_profiles = models.MyTardisProfile.objects.all()
        mytardis_urls = []
        for profile in mytaris_profiles:
            mytardis_urls.append(profile.url)
        return mytardis_urls








































import logging
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

from bdpindex.searchengine import models


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Load up the initial state of the database (replaces use of
    fixtures).  Assumes specific structure.
    """

    args = ''
    help = 'Setup an initial task structure.'

    def setup(self):
        confirm = raw_input("This will ERASE and reset the database.  Are you sure [Yes|No]")
        if confirm != "Yes":
            print "action aborted by user"
            return

        for ns, name, desc in [(models.ExperimentProfile.PROFILE_SCHEMA_NS,
                                "Experiment Schema", "Information about experiment"),
                               (models.MyTardisProfile.PROFILE_SCHEMA_NS,
                                "MyTardis Schema", "Schema for MyTardis profile"),
                               ]:
            sch, _ = models.Schema.objects.get_or_create(namespace=ns, name=name, description=desc)
            logger.debug("sch=%s" % sch)

        experiment_schema = models.Schema.objects.get(namespace=models.ExperimentProfile.PROFILE_SCHEMA_NS)
        mytardis_schema = models.Schema.objects.get(namespace=models.MyTardisProfile.PROFILE_SCHEMA_NS)

        self.PARAM_TYPE_SCHEMA = {'description': [models.ParameterName.STRING,
                                                  experiment_schema],
                                  'location': [models.ParameterName.STRING,
                                               experiment_schema],
                                  'curated_data_source': [models.ParameterName.STRING,
                                                             mytardis_schema],
                                  'remark': [models.ParameterName.STRING,
                                             mytardis_schema],
                                  }
        for name, param_type_schema in self.PARAM_TYPE_SCHEMA.items():
            param_type_schema = self.PARAM_TYPE_SCHEMA[name]
            type = param_type_schema[0]
            schema = param_type_schema[1]
            param_name, created = models.ParameterName.objects.get_or_create(
                schema=schema, name=name, type=type)
            if not created:
                models.ParameterName.objects.filter(name=name).update(type=type)
            logger.debug(param_name)


    def handle(self, *args, **options):
        self.setup()
        print "done"
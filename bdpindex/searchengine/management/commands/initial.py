
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

        self.group, _ = Group.objects.get_or_create(name="standarduser")
        self.group.save()

        #for model_name in ('experimentprofileparameter', 'experimentprofileparameterset'):
         #   print ('Model Name %s' % model_name)
            #add_model = Permission.objects.get(codename="add_%s" % model_name)
          #  change_model = Permission.objects.get(codename="change_%s" % model_name)
            #delete_model = Permission.objects.get(codename="delete_%s" % model_name)
            #self.group.permissions.add(add_model)
           # self.group.permissions.add(change_model)
            #self.group.permissions.add(delete_model)

        self.group.save()




        # Create the schemas for template parameters or config info
        # specfied in directive arguments
        for ns, name, desc in [(models.ExperimentProfile.PROFILE_SCHEMA_NS,
                                "bdp_index", "Information about "),

        ]:
            sch, _ = models.Schema.objects.get_or_create(namespace=ns, name=name, description=desc)
            logger.debug("sch=%s" % sch)

        experiment_schema = models.Schema.objects.get(namespace=models.ExperimentProfile.PROFILE_SCHEMA_NS)



        self.PARAMTYPE = {'description': models.ParameterName.STRING,
                          'location': models.ParameterName.STRING,
                          }

        for name, param_type in self.PARAMTYPE.items():
            param_name, created = models.ParameterName.objects.get_or_create(schema=experiment_schema,
                                                                       name=name,
                                                                       type=self.PARAMTYPE[name])
            if not created:
                models.ParameterName.objects.filter(name=name).update(type=param_type)
            logger.debug(param_name)


        print "done"

    def handle(self, *args, **options):
        self.setup()
        print "done"

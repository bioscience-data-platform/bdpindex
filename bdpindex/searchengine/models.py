from django.db import models
import logging


logger = logging.getLogger(__name__)


#declaration of a set of parameter (e.g., XML schema)
class Schema(models.Model):
    """ Representation of a set of parameters (equiv to XML Schema)

        :attribute namespace: namespace for this schema
        :attribute name: unique name
        :attribute description: displayable text describing the schema

    """
    namespace = models.URLField(verify_exists=False, max_length=400, help_text="A URI that uniquely ids the schema")
    name = models.SlugField(default="", help_text="A unique identifier for the schema")
    description = models.CharField(max_length=80, default="", help_text="The description of this schema")
    
    class Meta:
        unique_together = (('namespace', 'name'),)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.namespace)


class ParameterName(models.Model):
    """ A parameter associated with a schema

        :attribute schema: the  :class:`bdpindex.searchengine.models.Schema` which this parameter belongs to
        :attribute name: the name of the parameter
        :attribute type: the type of the parameter from TYPES
        :attribute ranking: int which indicates relative ranking in listings
        :attribute initial: any initial value for this parameter
        :attribute choices: a serialised python list of string choices for the STRLIST type
        :attribute help_text: text that appears in admin tool
        :attribute max_length: maximum length for STRING types
    """
    schema = models.ForeignKey(Schema, help_text="Schema that contains this parameter")
    name = models.CharField(max_length=50)
    # TODO: need to do this so that each paramter can appear only once
    # in each schema

    class Meta:
        unique_together = (('schema', 'name'),)
        ordering = ["-ranking"]

    UNKNOWN = 0
    STRING = 1
    NUMERIC = 2  # only integers
    LINK = 3
    STRLIST = 4
    DATE = 5
    YEAR = 6
    TYPES = (
        (UNKNOWN, 'UNKNOWN'),
        (STRING, 'STRING'),
        (NUMERIC, 'NUMERIC'),
        (LINK, 'LINK'),
        (STRLIST, 'STRLIST'),
        (DATE, 'DATE'),
        (YEAR, 'YEAR')

    )
    # The form used to store dates in the DATE type field
    DATE_FORMAT = "%b %d, %Y"

    type = models.IntegerField(choices=TYPES, default=STRING)

    ranking = models.IntegerField(default=0,
                                  help_text="Describes the relative ordering "
                                            "of parameters when displaying: the larger "
                                            "the number, the more prominent the results")
    initial = models.TextField(default="", blank=True,
                               verbose_name="Initial Value",
                               help_text="The initial value for this parameter")
    choices = models.TextField(default="", blank=True,
                               verbose_name="Choices for the field")
    help_text = models.TextField(default="", blank=True,
                                 verbose_name="Text to help user fill out "
                                              "the field")
    max_length = models.IntegerField(default=255,
                                     verbose_name="Maximum number of "
                                                  "characters in a parameter")

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.schema.name)

    #TODO: make a method to display schema and parameters as XML schema definition
    def get_type_string(self, val):
        for (t, str) in self.TYPES:
            if t == val:
                return str
        return "UNKNOWN"

    #TODO: Check MyTardis code base for consistency
    def get_value(self, val):
        #logger.debug("type=%s" % self.type)
        #logger.debug("val=%s" % val)
        res = val
        if self.type == self.STRING:
            res = val
        elif self.type == self.NUMERIC:
            try:
                res = int(val)
            except ValueError:
                logger.debug("invalid type")
                raise
        elif self.type == self.STRLIST:
            try:
                import ast
                res = ast.literal_eval(val)
                logger.debug('STRLIST %s length %d' % (res, len(res)))
            except ValueError:
                logger.debug("invalid type")
                raise
        else:
            logger.debug("Unsupported Type")
            raise ValueError
        return res


class ExperimentProfile(models.Model):
    experiment_id = models.IntegerField(help_text='Experiment ID')
    title = models.CharField(max_length=255, help_text='Experiment Title')
    #description = models.TextField(blank=True, help_text='Experiment Description')
    #location = models.CharField(max_length=255, help_text='Location of experiment data')

    PROFILE_SCHEMA_NS = "http://www.rmit.edu.au/schemas/experiment_profile"

    def __unicode__(self):
        return self.title


class ExperimentProfileParameterSet(models.Model):
    """
        Association of an experiment profile object with a schema
    """
    experiment_profile = models.ForeignKey(ExperimentProfile, unique=True,
                                           help_text='Information about experiment')
    schema = models.ForeignKey(Schema, verbose_name='Schema')
    ranking = models.IntegerField(default=0)

    class Meta:
        ordering = ['-ranking']


class ExperimentParameter(models.Model):
    """
        The values for some metadata for an Experiment profile
    """
    name = models.ForeignKey(ParameterName, verbose_name='Parameter name')
    paramset = models.ForeignKey(ExperimentProfileParameterSet,
                                 verbose_name='Parameter Set')
    value = models.TextField(blank=True, verbose_name='Parameter Value',
                             help_text='The value of this parameter')

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.paramset, self.value)

    def get_value(self,):
        try:
            val = self.name.get_value(self.value)
        except ValueError:
            logger.debug('Got bad value for paramter %s' % self.name)
            raise
        return val

    class Meta:
        ordering = ["name"]



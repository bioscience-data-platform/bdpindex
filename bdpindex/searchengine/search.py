from oaipmh.client import Client
from oaipmh import error
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from urllib2 import Request, urlopen, URLError, HTTPError

from bdpindex.searchengine import models
from bdpindex import settings

import pysolr
import json
import os
import logging


logger = logging.getLogger(__name__)
PYSOLR_SUFFIX = '_txt'


class ErrorBase(Exception):
    pass


class OAIPMHError(ErrorBase):
    """ The OAIPMH access failed"""
    pass


def search(search_phrase, index=False):
    solr = pysolr.Solr('http://115.146.86.217:8080/solr')#, timeout=10)
    if index:
        index_data(search_phrase)

    results = solr.search(search_phrase, **{'hl': 'true',
                                               'hl.fragsize': 10,})
    search_result = []
    for result in results:
        formatted_result = {}
        print 'result', result
        first_name = result['first_name' + PYSOLR_SUFFIX]
        last_name = result['last_name' + PYSOLR_SUFFIX]
        name = first_name[0] + " " + last_name[0]
        email = result['email' + PYSOLR_SUFFIX]
        title = result['experiment_title' + PYSOLR_SUFFIX]
        description = result['experiment_description' + PYSOLR_SUFFIX]
        url = result['experiment_url' + PYSOLR_SUFFIX]

        formatted_result['owner'] = name
        formatted_result['email'] = email[0]
        formatted_result['title'] = title[0]
        formatted_result['description'] = description[0]
        formatted_result['url'] = url[0]
        search_result.append(formatted_result)
    return search_result


def pull_data(source):
    list_of_records = []
    registry = MetadataRegistry()
    registry.registerReader('oai_dc', oai_dc_reader)
    # Get list of public experiments at sources
    registry = MetadataRegistry()
    registry.registerReader('oai_dc', oai_dc_reader)
    client = Client(source
                    + "/apps/oaipmh/?verb=ListRecords&metadataPrefix=oai_dc", registry)
    try:
        exps_metadata = [meta
                         for (header, meta, extra)
                         in client.listRecords(metadataPrefix='oai_dc')]
    except AttributeError as e:
        msg = "Error reading experiment %s" % e
        logger.error(msg)
        raise OAIPMHError(msg)
    except error.NoRecordsMatchError as e:
        msg = "no public records found on source %s" % e
        logger.warn(msg)
        return
    for exp_metadata in exps_metadata:
        user_id = exp_metadata.getField('creator')[0]
        user_profile = json.loads(_get_user(source, user_id))
        data_tobe_indexed = dict(user_profile)
        data_tobe_indexed['user_id'] = user_id

        exp_id = exp_metadata.getField('identifier')[0]
        description = exp_metadata.getField('description')[0]
        title = exp_metadata.getField('title')[0]
        if settings.EXPERIMENT_PATH[0] == '/':
            settings.EXPERIMENT_PATH = settings.EXPERIMENT_PATH[1:]
        experiment_url = os.path.join(source,
                                      settings.EXPERIMENT_PATH % exp_id)

        data_tobe_indexed['experiment_id'] = exp_id
        data_tobe_indexed['experiment_title'] = title
        data_tobe_indexed['experiment_description'] = description
        data_tobe_indexed['experiment_url'] = experiment_url
        data_tobe_indexed['id'] = experiment_url
        for k, v in data_tobe_indexed.items():
            logger.debug('%s = %s' % (k, v))
        logger.debug('')
        list_of_records.append(json.dumps(data_tobe_indexed))

    return list_of_records


def _get_user(source, user_id):
    """
    Retrieves information about the user_id at the source
    """
    try:
        xmldata = getURL("%s/apps/reposproducer/user/%s/"
                         % (source, user_id))
    except HTTPError:
        msg = "error getting user information"
        logger.error(msg)
        raise
    return xmldata


def getURL(source):
    request = Request(source, {}, {})
    response = urlopen(request)
    xmldata = response.read()
    return xmldata


def index_data(records):
    solr = pysolr.Solr(settings.PYSOLR_SERVER)
    record_to_index = []
    for record in records:
        encoded_record = dict(json.loads(record))
        new_dict = {}
        for k, v in encoded_record.items():
            dynamic_key = str(k) + PYSOLR_SUFFIX
            if k == 'id':
                dynamic_key = str(k)
            new_dict[dynamic_key] = str(v)
            logger.debug('k=%s v=%s' % (dynamic_key, v))
        record_to_index.append(new_dict)
    solr.add(record_to_index)
    solr.optimize()


def get_all_mytardis_deployment():
    mytaris_profiles = models.MyTardisProfile.objects.all()
    all_deployments = []
    for profile in mytaris_profiles:
        deployment = {'url': profile.url}
        deployment['institution'] = profile.institution
        try:
            paramsets = models.MyTardisProfileParameterSet \
                .objects.filter(mytardis_profile=profile)
            for paramset in paramsets:
            #deployment['']
                print 'paramset', paramset
                params = models.MyTardisParameter.objects.filter(parameter_set=paramset)
                for param in params:
                    name = str(param.name).split('(')
                    deployment[name[0]] = param.value
        except Exception, e:
            print e
        all_deployments.append(deployment)
    logger.debug('all_deployments=%s' % all_deployments)
    return all_deployments





















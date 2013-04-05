import pysolr


def index_data(search_phrase):

# Setup a Solr instance. The timeout is optional.
    solr = pysolr.Solr('http://115.146.86.217:8080/solr')#, timeout=10)

# How you'd index data.
    solr.add([
        {
            "id": "doc_1",
            "title": "The history of cats: Leopard",
            "description": 'The leopard (pron.: ), Panthera pardus, is a member' +\
                           'of the Felidae family and the smallest of the four "big cats" in' +\
                           'the genus Panthera, the other three being the tiger, lion, and jaguar.' +\
                           ' The leopard was once distributed across eastern and southern Asia' +\
                           ' and Africa, from Siberia to South Africa, but its range of distribution' +\
                           ' has decreased radically because of hunting and loss of habitat. '
            },
        {
            "id": "doc_3",
              "title": "Tiger: The ferocious cats from India",
              "description": "The tiger (Panthera tigris) is the largest cat species, reaching "
                             "a total body length of up to 3.3 metres (11 ft) and weighing up "
                             "to 306 kg (670 lb). It is the third largest land carnivore (behind "
                             "only the Polar bear and the Brown bear). I"
            },
        {
            "id": "doc_2",
            "title": "Hyena: Wild dogs",
            "description": "Hyenas or Hyaenas (from Greek) are the animals "
                           "of the family Hyaenidae (pron.: //) of suborder"
                           " feliforms of the Carnivora. It is the fourth smallest biological"
                           " family in the Carnivora (consisting of four species), and one "
                           "of the smallest in the mammalia."
            },

        ])

    # You can optimize the index when it gets fragmented, for better speed.
    solr.optimize()

    # Later, searching is easy. In the simple case, just a plain Lucene-style
    # query is fine.
    #queries = [search_phrase, 'tasty', 'iman', 'tast', 'banana']
    #result = []
    #for query in queries:
        #result.append(search(solr, query))

    #return result


def search(search_phrase, index_data=False):
    solr = pysolr.Solr('http://115.146.86.217:8080/solr')#, timeout=10)
    if index_data:
        index_data(search_phrase)

    results = solr.search(search_phrase, **{'hl': 'true',
                                               'hl.fragsize': 10,})

    # The ``Results`` object stores total results found, by default the top
    # ten most relevant results and any additional data like
    # facets/highlighting/spelling/etc.
    #print("Saw {0} result(s).".format(len(results)))

    # Just loop over it to access the results.
    #print '--- searching', search_phrase
    #print("Saw {0} result(s).".format(len(results)))
    formatted_result = []
    found = 'Found'
    if not results:
        found = 'Not Found'
    formatted_result.append(found)
    counter = 0
    for result in results:
        counter += 1
        title = result['title']
        description = result['description']
        print result
        #print "result %s" % result['title']

        #result = ("The title is '{0}'.".format(result['title']))
        #result = ("'{0}'.".format(result['title']))
        formatted_result.append("--RESULT: %d" % counter)
        formatted_result.append("--TITLE: %s" % title[0])
        formatted_result.append("--DESCRIPTION: %s" % description)
        # For a more advanced query, say involving highlighting, you can pass
        # additional options to Solr.
        #results = solr.search(search_phrase, **{
        #    'hl': 'true',
        #    'hl.fragsize': 10,
        #    })

        # You can also perform More Like This searches, if your Solr is configured
        # correctly.
        #similar = solr.more_like_this(q='id:doc_2', mltfl='text')

        # Finally, you can delete either individual documents...
        #solr.delete(id='doc_1')

        # ...or all documents.
        #solr.delete(q='*:*')
    return formatted_result
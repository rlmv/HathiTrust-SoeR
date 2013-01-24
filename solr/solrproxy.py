
import sys
import json
import argparse

import requests
try:
    from lxml import etree
except ImportError:
    import xml.etree.cElementTree as etree
    


SOLR_HOST = "http://chinkapin.pti.indiana.edu"
SOLR_PORT = 9994
SOLR_STUB = "/solr/select/"
solrbaseurl = "".join([SOLR_HOST, ":", str(SOLR_PORT), SOLR_STUB])


def query(querystring, rows=10, start=0, fields=[], json=True):
    """
    Arguments:
        rows: the maximum number of results to return
        fields: an iterable of fields to return with the
            response, eg. fl=['title', 'author']
        json: true by default  - returns the JSON object,
            or, if false, returns an xml tree.

    Return:
        JSON resource, or lxml etree.
    """
    terms = {}
    terms['q'] = querystring
    terms['rows'] = rows
    terms['start'] = start
    terms['qt'] = 'sharding'

    if json:
        terms['wt'] = 'json'

    if fields:
        terms['fl'] = ','.join(fields)

    r = requests.get(solrbaseurl, params=terms)
    r.raise_for_status()

    if json:
        return r.json()

    return etree.fromstring(r.content)


def iterquery(querystring, rows=10, fields=[]):
    """ Defines an generator over a query.
    
        This lets you stick the query in a for loop
        and iterate over all the results, like so:
        
        >>> for doc in iterquery(<querystring>):
        ...     print json.dumps(doc, indent=4)
        
        The return docs are python-interpreted json
        structures - the SOLR api spec defines the
        available fields:
        http://wiki.htrc.illinois.edu/display/COM/2.+Solr+API+User+Guide
        
        For now, errors get passed up from the query
        function...TODO: implement some handling.
    """
    
    num_retrieved = 0
    new_iter = True
    num_found = None
    
    """" need to iteate over ['response']['docs']"""
    
    while True:
        # send a query, then iterate over ['response']['docs']
        result = query(querystring, rows=rows, start=num_retrieved, fields=fields, json=True)
        
        if new_iter:
            num_found = result['response']['numFound']
            new_iter = False
        
        if num_found == num_retrieved:
            raise StopIteration
            
        for doc in result['response']['docs']:
            num_retrieved += 1
            
            yield doc



def jsonquery():
    pass

def xmlquery():
    pass


def getnumfound(querystring):
    """ Return the total number oqf matches for the query. """
    return int(query(querystring, rows=0, json=True)['response']['numFound'])


def getallids(querystring):
    """ Return an generator over all the document ids that
        match querystring."""
    for doc in iterquery(querystring, fields=['id']):
        yield doc['id']


def getmarc():
    base = "http://chinkapin.pti.indiana.edu:9994/solr/MARC/?volumeIDs="

    ids = ['mdp.39015062319309', 'mdp.39015026997125', 'uc1.31822021576848']
    idstring = "|".join(volid for volid in ids)
    
    url = base + idstring
    print url
    r = requests.get(url)
    r.raise_for_status()
    
    with open('marc.zip', 'wb') as f:
        f.write(r.content)






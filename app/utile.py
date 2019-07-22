"""This module will encode and parse the query string params."""

from urlparse import parse_qs
import logging

def parse_url_query_params(query_string):
    """
        method is to parse the url query parameter string.
    """
    logging.debug('Inside parse_url_query_params method')
    # Parse the query param string
    url_query_params = dict(parse_qs(query_string))
    # Get the value from the list
    query_params = {key: value[0] for key, value in url_query_params.items()}
    return query_params

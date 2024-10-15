from django.test import TestCase
from . import request_functions

def test_input_url(url):
    domain = 'https://wikipedia.org/'
    cut_url = url[:8]+url[11:]
    if domain not in cut_url:
        return False
    if request_functions.status_code(domain) != 200 and request_functions.status_code(domain) != 200:
        return False
    if request_functions.status_code(url) != 200:
        return False
    if not request_functions.is_valid_url(url):
        return False
    
    return True
from django.shortcuts import render
from . import my_forms
from . import tests
from . import request_functions
from collections import deque

# Create your views here.
def home(request):
    context = {}
    search_form = my_forms.QueryWikiForm()
    context['search_form'] = search_form
    return render(request, 'home.html', context)

def search(request):
    if request.method == 'POST':
        start_url = request.POST["url_wiki_user_input"]
        print(start_url)
        if tests.test_input_url(start_url):
            result = request_functions.crawl(start_url)
    return render(request, 'result.html', {'result':result})
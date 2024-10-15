from django.forms import ModelForm
from .models import SearchForm

class QueryWikiForm(ModelForm):
    class Meta:
        model = SearchForm
        fields = '__all__'
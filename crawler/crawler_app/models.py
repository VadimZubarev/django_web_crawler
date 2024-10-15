from django.db import models

class SearchForm(models.Model):
    given_wiki_url = models.CharField(max_length=255)

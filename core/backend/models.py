from django.db import models
from django.utils import timezone


class Election(models.Model):
    '''Models for creating elections'''
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_of_election = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    '''Model to create and manage portfolios'''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    '''Model to create and manage cnadidates'''
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank=True)
    picture = models.ImageField(upload_to='pictures', null=True, blank=True)
    ballot_number = models.IntegerField(default=1)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

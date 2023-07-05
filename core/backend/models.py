from django.db import models
from django.utils import timezone


class Election(models.Model):
    '''Models for creating elections'''
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_of_election = models.DateTimeField(default=timezone.now)  # noqa
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    '''Model to create and manage cnadidates'''
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, blank=True)  # noqa
    house = models.CharField(max_length=20, null=True, blank=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    picture = models.ImageField(upload_to='pictures', null=True, blank=True)
    ballot_number = models.IntegerField(default=1)
    vote_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    # YES / NO VOTES
    no_votes_count = models.IntegerField(default=0)  # for when voter is alone

    def get_vote_percentage(self):
        '''Returns the percentage of (YES) votes for a candidate'''
        if self.vote_count == 0:
            return 0
        if self.position.get_votes_cast() == 0:
            return 0
        if self.no_votes_count == 0:
            return round((self.vote_count / self.position.get_votes_cast()) * 100, 2)  # noqa
        else:
            return round(self.vote_count / (self.vote_count + self.no_votes_count) * 100, 2)  # noqa

    def get_no_vote_percentage(self):
        '''Returns the percentage of NO votes for a candidate'''
        if self.no_votes_count == 0:
            return 0
        else:
            return round((self.no_votes_count / (self.vote_count + self.no_votes_count)) * 100, 2)  # noqa

    def __str__(self):
        return self.name


class Position(models.Model):
    '''Model to create and manage positions'''
    name = models.CharField(max_length=100, unique=True)
    precedence = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_candidates(self):
        '''Returns the number of candidates for the given position'''
        return Candidate.objects.filter(position=self).count()

    def get_votes_cast(self):
        '''Returns the total votes cast for this position'''
        cadidates = Candidate.objects.filter(position=self)
        return sum([candidate.vote_count for candidate in cadidates])

    def __str__(self):
        return self.name

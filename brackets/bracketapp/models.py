from django.db import models
from django.forms import ModelForm
class Bracket(models.Model):
    MAXNUM_CHOICES = (
    (2,"2"),
    (4,"4"),
    (8,"8"),
    (16,"16"),
    )
    tourny_round = models.IntegerField(default = 1)
    title = models.CharField(max_length=50)
    maxnum = models.IntegerField(choices=MAXNUM_CHOICES)
    def __unicode__(self):
        return self.title
    def get_num_competitions(self):
        return self.maxnum / 2
    def next_round(self):
        self.tourny_round += 1
class Competitor(models.Model):
    
    bracket = models.ForeignKey(Bracket)
    name = models.CharField(max_length=30)
    seed = models.IntegerField()
    def __unicode__(self):
        return self.name


class Competition(models.Model):
    tourny_round = models.IntegerField(default = 1)
    bracket = models.ForeignKey(Bracket)
    competitor_a = models.ForeignKey(Competitor,related_name="competitor_a_set")
    competitor_b = models.ForeignKey(Competitor,related_name="competitor_b_set")
    winner = models.ForeignKey(Competitor,null=True,blank=True,related_name="win_set")
    
    def __unicode__(self):
        return "[%s] %s vs %s" % (self.bracket,self.competitor_a, self.competitor_b)

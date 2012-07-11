from django.db import models
from django.forms import ModelForm
class Bracket(models.Model):

    maxnum_of_competitors  = models.IntegerField()
    time = models.DateTimeField()
    title = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.title

class Competitor(models.Model):

    bracket = models.ManyToManyField(Bracket)
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Competition(models.Model):

    competitor_a = models.ForeignKey(Competitor,related_name="competition_competitor_a_set")
    competitor_b = models.ForeignKey(Competitor,related_name="competition_competitor_b_set")
    bracket = models.ForeignKey(Competitor)
    
    def __unicode__(self):
        return u'%s vs %s' % (self.competitor_a, self.competitor_b)

class BracketForm(ModelForm):
    class Meta:
        model = Bracket



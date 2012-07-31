from django.db import models
from django.forms import ModelForm
class Bracket(models.Model):
    title = models.CharField(max_length=50)
    maxnum = models.IntegerField(choices=[(x, x) for x in range(1, 16)])
    def __unicode__(self):
        return self.title


class Competitor(models.Model):
    
    bracket = models.ForeignKey(Bracket)
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

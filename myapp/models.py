from __future__ import unicode_literals
from django.conf import settings
from django.db import models

# Create your models here.
class Dreamreal(models.Model):
     id = models.IntegerField(primary_key=True,  null=False)
     host = models.CharField(max_length=50, null=False)
     date = models.DateField()
     din = models.CharField(max_length=50, null=False)
     dout = models.CharField(max_length=50, null=False)
     dtot = models.CharField(max_length=50, null=False)
     class Meta:
         db_table = "dreamreal"
     def __str__(self):
          return str(self.id)+'::'+self.host+'::'+str(self.date)+'::'+str(self.din)+'::'+str(self.dout)+'::'+str(self.dtot)


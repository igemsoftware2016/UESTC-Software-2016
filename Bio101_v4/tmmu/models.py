from __future__ import unicode_literals
from django.db import models

class Input(models.Model):
    input1 = models.FloatField()
    input2 = models.FloatField()

    def __unicode__(self):
        return self.title

class File(models.Model):
	"""docstring for File"""
	file_name = models.CharField(max_length = 30)
	file_load = models.FileField(upload_to = './upload/')

	def __init__(self,):
		super(File, self).__init__()
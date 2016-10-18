#from __future__ import unicode_literals
from django.db import models


class Encode(models.Model):
	encode_token  = models.CharField(max_length = 256)
	encode_file   = models.FileField(upload_to = 'upload')

	def __str__(self):
		return self.encode_file.name

	def __unicode__(self):
		return self.encode_file.name

class Decode(models.Model):
	decode_token  = models.CharField(max_length = 256)
	decode_file   = models.FileField(upload_to = 'upload')

	def __str__(self):
		return self.decode_file.name

	def __unicode__(self):
		return self.decode_file.name

# class Decode2(object):
# 	fragment  = models.TextField()
# 	decode_token  = models.CharField(max_length = 256)	

class Edit(models.Model):
	edit_token1  = models.TextField()
	edit_token2  = models.TextField()


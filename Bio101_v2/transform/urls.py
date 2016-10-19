from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name = 'home'),
	url(r'^home/$', views.home, name = 'home'),
	url(r'^eupload/$', views.upload_encode, name = 'upload_encode'),
	url(r'^dupload/$', views.upload_decode, name = 'upload_decode'),
	url(r'^endownload/$', views.endownload, name = 'endownload'),
	url(r'^dedownload/$', views.dedownload, name = 'dedownload'),
	url(r'^eblast/$', views.eblast, name = 'eblast'),
	# url(r'^blast/$', views.upload_blast, name = 'upload_blast'),
	# url(r'^bldownload/$', views.bldownload, name = 'bldownload'),

]

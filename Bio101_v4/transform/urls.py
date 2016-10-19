from django.conf.urls import url
from . import views

urlpatterns = [ 
	url(r'^$', views.index, name = 'index'),
	url(r'^home/$', views.index, name = 'home'),
	url(r'^encode/$', views.encode, name = 'encode'),
	url(r'^decode/$', views.decode, name = 'decode'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^edit/$', views.edit, name = 'edit'),
	url(r'^editted/$', views.editted, name = 'editted'),
	url(r'^download/(?P<file_name>.+)/$', views.download, name = 'download'),
]

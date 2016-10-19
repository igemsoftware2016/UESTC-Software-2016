from django.conf.urls import url
from tmmu import views
from tmmu import chart

urlpatterns = [
    url(r'^$', 	            views.index,            name='index'),
    url(r'^download/$',     views.download,       name='download'),
    url(r'^upload/$',       views.upload_file,      name='upload'),
    url(r'^upload_num/$',   views.upload_num,       name='upload_num'),
    # url(r'^chart/simple.png$', chart.simple,name='chart'),
]


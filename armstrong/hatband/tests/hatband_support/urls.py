from django.conf.urls.defaults import patterns, include, url

from armstrong import hatband as admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
)

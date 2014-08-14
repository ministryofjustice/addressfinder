from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from address import views


router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'addressfinder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/', include(router.urls)),

    url(r'^admin/', include(admin.site.urls)),
)

"""whatsbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from wbot import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$',views.login),
    url(r'^dashboard/',views.dashboard,name='list'),
    url(r'^registerBot/$',views.registerbot),
    url(r'sendotp/',views.sendOtp),
    url(r'messages/$',views.messages),
    url(r'messages/(?P<pk>[0-9]+)/',views.messageDetails),
    url(r'logout/',views.logout_view),
    # url(r'media/',views.mediafetch),
    url(r'accounts/login/',views.login),
    url(r'^upload/',views.list,name='list'),
    url(r'^compose/',views.compose_message),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

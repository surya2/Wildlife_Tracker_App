"""
URL configuration for b03_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from oauth_app import views


class CustomTemplateView(TemplateView):
   template_name = "index.html"

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       try:
           # Replace 'google' with the name of your social provider as configured in settings.py
           provider_id = 'google'
           provider = self.request.user.socialaccount_set.get(provider=provider_id)
           google_login = provider.get_adapter().get_login_url(self.request, provider)
           context['google_login'] = google_login
       except (OAuth2Error, AttributeError):
           context['google_login'] = None
       return context


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", include("oauth_app.urls")),
    path('map',views.map, name="map"),
    #path('<slug:slug>/', views.post_detail, name='post_detail')
    #path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico')))
    #path('route',views.route, name="route"),


]

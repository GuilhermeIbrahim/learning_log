from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', RedirectView.as_view(url='/accounts/login/', permanent=False), name='login'),
    path('logout/', RedirectView.as_view(url='/accounts/logout/', permanent=False), name='logout'),
    path('register/', RedirectView.as_view(url='/accounts/signup/', permanent=False), name='register'),
]
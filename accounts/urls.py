from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import signup  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='Login'),
    path('logout/', auth_views.LogoutView.as_view(), name='Logout'),
    path('signup/', signup, name='signup'),
    
]
  


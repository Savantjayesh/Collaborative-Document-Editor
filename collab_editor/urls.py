from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('dashboard')),
    path('admin/', admin.site.urls),
    path('editor/', include('editor.urls')),
    path('auth/', include('users.urls')),  
]

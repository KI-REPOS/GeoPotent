from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('potential_app.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]
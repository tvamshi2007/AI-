from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ai/',    include('voiceai.urls')),
    path('',       include('crudapp.urls')),
]

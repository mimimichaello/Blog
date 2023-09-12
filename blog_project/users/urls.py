from django.urls import path
from users.views import register
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name= 'users'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

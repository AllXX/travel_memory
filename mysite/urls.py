from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('memory.urls'),name='memorys'),
    path('',include('blog.urls'),name='blogs')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

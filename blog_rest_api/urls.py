from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/articles/', include('articles.api.urls', namespace='articles-api')),
    path('api/categories/', include('categories.api.urls', namespace='categories-api')),
    path('api/comments/', include('comments.api.urls', namespace='comments-api'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
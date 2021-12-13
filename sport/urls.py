
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',include('dashboard.urls')),
    path('',include('sportapp.urls')),
    path('clientportal/',include('clientportal.urls')),
    path('api/v1/', include('apis.urls')),
]

urlpatterns += i18n_patterns(

    path('dashboard/',include('dashboard.urls')),
    path('',include('sportapp.urls')),
    path('clientportal/',include('clientportal.urls')),
    path('api/v1/', include('apis.urls')),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

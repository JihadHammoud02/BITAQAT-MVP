from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('org/', include('Club.urls')),
    path('guest/', include('Fan.urls')),
    path('', include('django.contrib.auth.urls'))
    # path("debug/", include(debug_toolbar.urls)),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

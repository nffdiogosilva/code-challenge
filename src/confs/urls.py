from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from stock.views import CompanyViewSet, DailyPriceViewSet, RecommendationViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'dailyprices', DailyPriceViewSet)
router.register(r'recommendations', RecommendationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    from django.views import defaults

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('500/', defaults.server_error),
        path('403/', defaults.permission_denied),
        path('404/', defaults.page_not_found),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

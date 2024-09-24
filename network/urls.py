from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('networks', views.NetworkViewSet, basename='network')

urlpatterns = [*router.urls]

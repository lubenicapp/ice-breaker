from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('networks', views.NetworkViewSet, basename='network')

urlpatterns = [
    *router.urls,
    path('persons/', views.person_view, name='person-view'),
    path('me/', views.me, name='me-view'),
    path('graph/', views.graph, name='graph-view'),
]

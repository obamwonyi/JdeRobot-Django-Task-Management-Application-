from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet, index

router = DefaultRouter()
router.register( "tasks", TaskViewSet, basename='task')
router.register("categories", CategoryViewSet, basename='category')

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
]
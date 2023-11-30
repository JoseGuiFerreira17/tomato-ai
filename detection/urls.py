from django.urls import path
from .views import TomatoDetectionView

urlpatterns = [
    path('detect/', TomatoDetectionView.as_view(), name='detect'),
]
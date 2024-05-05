from django.urls import path
from .views import TrainingInfoView

urlpatterns = [
    path('training-info/', TrainingInfoView.as_view(), name='training-info'),
]
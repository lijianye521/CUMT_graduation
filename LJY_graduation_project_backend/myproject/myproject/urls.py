"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from .views import protected_view ,list_datasets,hello_world_view,predict,list_models# 确保从你的views模块正确导入视图函数
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('upload/', protected_view, name='protected'),
    path('sql/', include('managesql.urls')),#让其包含sql功能的路由  
    path('api/datasets/', list_datasets, name='list-datasets'),
    path('api/models/', list_models, name='list-models'),
    path('hello/', hello_world_view,name="hello"),  # 添加这行
    path('api/predict/', predict, name='predict'),





] + static('/dataset/', document_root='myproject/dataset')

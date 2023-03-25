from django.urls import path, include  
from rest_framework import routers  
from . import views  

router = routers.DefaultRouter()  
router.register('qr', views.QrViewSet, "")  
app_name = 'apiv1' 

urlpatterns = [
    path('qr/', views.QrViewSet.as_view(), name='qr'),
    ] 

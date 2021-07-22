  
from django.urls import path
from gms_admin.views import inbox

urlpatterns = [
   	path('', inbox, name='inbox'),


]
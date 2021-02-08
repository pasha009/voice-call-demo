from django.urls import path

from .views import index, call_view, test_index, test_call_view
  
urlpatterns = [ 
    path('', index), 
    path('call/<str:room_id>', call_view, name="call_view"),
    path('test/', test_index), 
    path('test/call/<str:room_id>', test_call_view, name="test_call_view"),
] 

from django.urls import path
from .views import (
    DevicesView,
    DeviceView,
)

urlpatterns = [
    path('devices/', DevicesView.as_view()),
    path('devices/<int:pk>/', DeviceView.as_view()),
]

# urlpatterns = [
#     path('device/', DeviceView.as_view(), name='device'),
#     path('device/create/', DeviceTokenView.as_view(), name='device_token'),
#     path('device/token/deactivate/', DeviceTokenStatusView.as_view(), name='device_token_status'),
#     path('device-token/', DeviceTokenView.as_view(), name='device-token'),
#     path('device-token-status/', DeviceTokenStatusView.as_view(), name='device-token-status'),
#     path('device-status/', DeviceStatusView.as_view(), name='device-status'),
# ]
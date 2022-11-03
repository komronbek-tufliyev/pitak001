from django.urls import path

# Order views
from .views import (
    OrderList,
    OrderDetail,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
)

# OrderComment views
from .views import (
    OrderCommentList,
    OrderCommentDetail,
    OrderCommentCreateView,
    OrderCommentUpdateView,
    OrderCommentDeleteView,
)

# Places views
from .views import (
    PlaceList,
    PlaceDetail,
    PlaceView,
)

urlpatterns = [
    path('orders/', OrderList.as_view()),
    path('orders/<int:pk>/', OrderDetail.as_view()),
    path('orders/create/', OrderCreateView.as_view()),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view()),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view()),
    path('orders/<int:pk>/comments/', OrderCommentList.as_view()),
    path('orders/<int:pk>/comments/<int:comment_pk>/', OrderCommentDetail.as_view()),
    path('orders/<int:pk>/comments/create/', OrderCommentCreateView.as_view()),
    path('orders/<int:pk>/comments/<int:comment_pk>/update/', OrderCommentUpdateView.as_view()),
    path('orders/<int:pk>/comments/<int:comment_pk>/delete/', OrderCommentDeleteView.as_view()),
    path('places/', PlaceList.as_view()),
    path('places/<int:pk>/', PlaceDetail.as_view()),    
    path('places/create/', PlaceView.as_view()),
    
]
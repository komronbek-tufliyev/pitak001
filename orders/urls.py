from django.urls import path

# Order views
from .views import (
    OrderList,
    OrderDetail,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    LikedOrdersView,
    ListLikedOrders,
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
    path('orders/create/', OrderCreateView.as_view({'post': 'create'})),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view()),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view()),
    # path('orders/<int:pk>/comments/', OrderCommentList.as_view()),
    # path('orders/<int:pk>/comments/<int:comment_pk>/', OrderCommentDetail.as_view()),
    # path('orders/<int:pk>/comments/create/', OrderCommentCreateView.as_view()),
    # path('orders/<int:pk>/comments/<int:comment_pk>/update/', OrderCommentUpdateView.as_view()),
    # path('orders/<int:pk>/comments/<int:comment_pk>/delete/', OrderCommentDeleteView.as_view()),
    path('places/', PlaceList.as_view()),
    path('places/<int:pk>/', PlaceDetail.as_view()),    
    path('places/create/', PlaceView.as_view()),
    path('orders/user/liked/', LikedOrdersView.as_view(), name='liked-order'),
    path('orders/user/liked/<int:order_id>/', LikedOrdersView.as_view(), name='post-liked-order'),
    path('orders/liked/', ListLikedOrders.as_view(), name='list-liked-orders'),
    
]
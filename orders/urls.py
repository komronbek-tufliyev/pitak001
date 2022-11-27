from django.urls import path

from .views import show_filtered_orders, show_my_orders

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
    FavOrderView,
)

# filtered order views 
from .views import(
    MyOrdersListView,
    Orders4DriverView,
    Orders4NonDriverView,
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
    path('orders/favourite/', FavOrderView.as_view(), name='list-favourites'),
    # path('orders/favourite/add/', FavOrderView.as_view(), name='post-favourite'),
    # path('orders/favourite/delete/', FavOrderView.as_view(), name='delete-favourite'),

    # filtered orders by place
    path('orders/filter/<str:from_place>/<str:to_place>/<str:tuman>/', show_filtered_orders, name='show_filtered_orders'),
    path('orders/my-orders/', MyOrdersListView.as_view(), name='my-orders'),

    # Filtered orders by is_driver
    path('orders/for-driver/', Orders4DriverView.as_view(), name='orders-for-driver'),
    path('orders/for-non-driver/', Orders4NonDriverView.as_view(), name='orders-for-non-driver'),
]
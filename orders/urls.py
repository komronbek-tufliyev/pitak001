from django.urls import path

# from .views import show_filtered_orders, show_my_orders

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
    # OrderCommentList,
    # OrderCommentDetail,
    # OrderCommentCreateView,
    # OrderCommentUpdateView,
    # OrderCommentDeleteView,
    FavOrderView,
)

# filtered order views 
from .views import(
    MyOrdersListView,
    Orders4DriverView,
    Orders4NonDriverView,
    FilteredOrders4DriverView,
    FilteredOrders4NonDriverView,
    FilterByRegionView,
    AddresbyFilter4Driver,
    AddresbyFilter4nonDriver,
)

# Places views
from .views import (
    PlaceList,
    PlaceDetail,
    PlaceView,
)

from orders.order_views.book_seat_view import BookSeatView

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
    # path('places/<int:pk>/', PlaceDetail.as_view()), 
    path('places/filter-by/<str:region>/', FilterByRegionView.as_view(), name='filter-by-region'), 
    path('places/create/', PlaceView.as_view()),
    path('orders/favourite/', FavOrderView.as_view(), name='list-favourites'),
    # path('orders/favourite/add/', FavOrderView.as_view(), name='post-favourite'),
    # path('orders/favourite/delete/', FavOrderView.as_view(), name='delete-favourite'),

    path('orders/book-seat/<int:pk>/', BookSeatView.as_view(), name='book-seat'),

    # show my orders
    path('orders/my-orders/', MyOrdersListView.as_view(), name='my-orders'),

    # Filtered orders by is_driver
    path('orders/for-driver/', Orders4DriverView.as_view(), name='orders-for-driver'),
    path('orders/for-non-driver/', Orders4NonDriverView.as_view(), name='orders-for-non-driver'),

    # filter by place
    path('orders/for-driver/filter/<str:from_place>/<str:to_place_region>/<str:to_place_district>/', FilteredOrders4DriverView.as_view(), name='orders-for-driver'),
    path('orders/for-non-driver/filter/<str:from_place>/<str:to_place_region>/<str:to_place_district>/', FilteredOrders4NonDriverView.as_view(), name='orders-for-non-driver'), 
    

    # filter by from_place and to_place_region
    path('orders/for-driver/filter/<str:from_place>/<str:to_place_region>/', AddresbyFilter4Driver.as_view(), name='filterla'),
    path('orders/for-non-driver/filter/<str:from_place>/<str:to_place_region>/', AddresbyFilter4nonDriver.as_view(), name='laslka')
]
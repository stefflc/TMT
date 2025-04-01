
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrdersWithinDateRangeView

urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path("date-range/", OrdersWithinDateRangeView.as_view(), name="orders-by-date-range"),
]
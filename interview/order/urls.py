
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrdersByTagView

urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path("tags/<int:tag_id>/orders/", OrdersByTagView.as_view(), name="orders-by-tag"),
]
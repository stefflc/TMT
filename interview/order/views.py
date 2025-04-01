from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrdersByTagView(APIView):
    """
    Return all orders associated with a specific tag.
    GET /tags/<tag_id>/orders/
    """
    def get(self, request, tag_id, *args, **kwargs):
        try:
            tag = OrderTag.objects.get(pk=tag_id)
        except OrderTag.DoesNotExist:
            return Response({"error": "Tag not found."}, status=status.HTTP_404_NOT_FOUND)

        orders = tag.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)
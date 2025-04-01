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



class OrderTagsListView(APIView):
    """
    Return all tags associated with a specific Order.
    GET /orders/<order_id>/tags/
    """
    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        tags = order.tags.all()
        serializer = OrderTagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

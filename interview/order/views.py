from rest_framework import generics, status
from rest_framework.response import Response

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

# originally chose OrderDeactiveView to align with existing naming conventions. Request is for DeactivateOrderView which could be harder to find.
class DeactivateOrderView(generics.UpdateAPIView):
    """
    Disable a specific order based on order id/pk.
    Sets IsActiveModel.is_active = False
    e.g. POST /orders/42/deactivate/ to use

    """
    queryset = Order.objects.all()
    lookup_field = "pk"  # default, just explicit here

    def update(self, request, *args, **kwargs):
        try:
            # IsActiveModel.activate has no rails to keep it honest... let's help it out.
            order = self.get_object()
        except (ValueError, TypeError):
            return Response({"error": "Invalid ID format. Must be an integer."}, status=400)
        except Order.DoesNotExist:
            # e.g. orders/9999999999/deactivate/ is invoked.
            return Response({"error": "Order not found."}, status=404)

        if not order.is_active:
            # chose 200 for this case as the result is to deactivate, and the pk would be deactivated
            return Response({"detail": "Order is already inactive."}, status=status.HTTP_200_OK)

        # order is activate
        deactivated = Order.deactivate(order.pk)
        if deactivated:
            return Response({"detail": f"Order {order.pk} deactivated."}, status=status.HTTP_200_OK)
        else:
            # if we're this far in the code, order.is_active is True, but deactivate() returned 0 count.
            return Response({"error": f'{order.pk} is activate, but deactivation attempt did not succeed.'}, status=400)
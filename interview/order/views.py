import datetime

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


# in hindsight, I probably would have used ListAPIView and overridden get_queryset, but I'm going fast here.
class OrdersWithinDateRangeView(APIView):
    """
    List orders where both start_date and embargo_date fall between given values.

    Example:
    GET /orders/date-range/?start_date=2024-03-01&embargo_date=2024-03-31
    """
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        # make sure to use .get to gracefully handle default case i.e. None
        start_date_param = request.query_params.get('start_date')
        embargo_date_param = request.query_params.get('embargo_date')
        date_format = "%Y-%m-%d"

        if not start_date_param or not embargo_date_param:
            return Response(
                {"error": "Both start_date and embargo_date are required in YYYY-MM-DD format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # ensure we have date objects to match models.DateField()

            start_date = datetime.strptime(start_date_param, date_format).date()
            embargo_date = datetime.strptime(embargo_date_param, date_format).date()
        except ValueError:
            return Response(
                {"error": f"Dates must be in {date_format} i.e. YYYY-MM-DD format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if embargo_date < start_date:
            return Response(
                {"error": "embargo_date cannot be earlier than start_date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # interpreting "between" as being inclusive of the start or end dates
        # update to gt/lt if you do not want inclusive start_date or embargo_date
        # could also add support for either start_date OR embargo_date (i.e. only one of the two is passed)
        orders = Order.objects.filter(
            start_date__gte=start_date,
            embargo_date__lte=embargo_date
        )

        if not orders.exists():
            # add a helper response. Could delete if front end correctly handles [] response.
            return Response({"detail": f"No orders found between {start_date} and {embargo_date}."},
                            status=200)

        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data, status=200)
import datetime

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from interview.inventory.models import Inventory, InventoryLanguage, InventoryTag, InventoryType
from interview.inventory.schemas import InventoryMetaData
from interview.inventory.serializers import InventoryLanguageSerializer, InventorySerializer, InventoryTagSerializer, InventoryTypeSerializer


class InventoryListCreateView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            metadata = InventoryMetaData(**request.data['metadata'])
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        
        request.data['metadata'] = metadata.dict()
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)
        
        return Response(serializer.data, status=200)
    
    def get_queryset(self):
        return self.queryset.all()


# Going fast, but this could probably just be an inherited class of InventoryListCreateview(...)
    # Did not want to grant InventoryListByDateView an explicit post() function which would be inherited
# Also considered overriding InventoryListCreateView.get() function but that view seems explicitly for getting all.

class InventoryListByDateView(APIView):
    """
    e.g. /inventory/?created_after=2024-01-01
    Pass the query param created_after to filter on the created_at field from TimestampedModel
    """
    queryset = Inventory.objects.all()
    # the base InventorySerializer class doesn't show created_at date field. If required, add a new serializer that has that field serialized.
    serializer_class = InventorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        created_after = request.query_params.get('created_after')

        if created_after:
            date_format = "%Y-%m-%d"
            # assumed date type based on "certain day" in requirements. Datetime would likely be useful given created_at is DateTimeField.
            try:
                # Parse string into datetime at 00:00:00
                created_after_dt = datetime.strptime(created_after, date_format)
                inventories = self.queryset.filter(created_at__gt=created_after_dt)
            except ValueError:
                return Response(
                    {'error': f'Invalid date format. Use {date_format} i.e. YYYY-MM-DD.'},
                    status=400
                )
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        else:
            inventories = self.queryset.all()

        serializer = self.serializer_class(inventories, many=True)
        return Response(serializer.data, status=200)
    

class InventoryRetrieveUpdateDestroyView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory)
        
        return Response(serializer.data, status=200)
    
    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=200)
    
    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        inventory.delete()
        
        return Response(status=204)
    
    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryTagListCreateView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)
        
        return Response(serializer.data, status=200)
    
    def get_queryset(self):
        return self.queryset.all()


class InventoryTagRetrieveUpdateDestroyView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory_tag)
        
        return Response(serializer.data, status=200)
    
    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory_tag, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=200)
    
    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs['id'])
        inventory_tag.delete()
        
        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryLanguageListCreateView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)
        
        return Response(serializer.data, status=200)
    
    def get_queryset(self):
        return self.queryset.all()


class InventoryLanguageRetrieveUpdateDestroyView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory)
        
        return Response(serializer.data, status=200)
    
    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=200)
    
    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        inventory.delete()
        
        return Response(status=204)
    
    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)
    

class InventoryTypeListCreateView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)
        
        return Response(serializer.data, status=200)
    
    def get_queryset(self):
        return self.queryset.all()


class InventoryTypeRetrieveUpdateDestroyView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory)
        
        return Response(serializer.data, status=200)
    
    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=200)
    
    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        inventory.delete()
        
        return Response(status=204)
    
    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)
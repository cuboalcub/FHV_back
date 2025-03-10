from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Rack
from .serializers import RackSerializer
from .services import RackService
from django.shortcuts import render

# Create your views here.
# This acts as the controller.
class RackViewSet(viewsets.ViewSet):
    def list(self, request):
        racks = RackService.get_all_racks()
        serializer = RackSerializer(racks, many = True)
        
        return Response(serializer.data)
    
    def retrieve(self, request, pk = None):
        try: 
            rack = RackService.get_rack_by_id(pk)
            serializer = RackSerializer(rack)
            
            return Response(serializer.data)
        except Rack.DoesNotExist:
            return Response({"error": "Rack not found"}, status = status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        serializer = RackSerializer(data = request.data)
        
        if serializer.is_valid():
            rack = RackService.create_rack(**serializer.validated_data)
            
            return Response(RackSerializer(rack).data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk = None):
        try: 
            rack = RackService.get_rack_by_id(pk)
            serializer = RackSerializer(rack, data = request.data, partial = False)
            
            if serializer.is_valid():
                rack = RackService.update_rack(pk, **serializer.validated_data)
                
                return Response(RackSerializer(rack).data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Rack.DoesNotExist:
            return Response({"error": "Rack not found"}, status = status.HTTP_404_NOT_FOUND)
        
    def partial_update(self, request, pk = None):
        try:
            rack = RackService.get_rack_by_id(pk)
            serializer = RackSerializer(rack, data = request.data, partial = True) 
            
            if serializer.is_valid():
                rack = RackService.update_rack(pk, **serializer.validated_data)
                
                return Response(RackSerializer(rack).data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Rack.DoesNotExist:
            return Response({"error": "Rack not found"}, status = status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk = None):
        try: 
            rack = RackService.delete_rack(pk)
            
            return Response({"message": "Rack deleted successfully"}, status = status.HTTP_204_NO_CONTENT)
        except Rack.DoesNotExist:
            return Response({"error": "Rack not found"}, status = status.HTTP_404_NOT_FOUND)
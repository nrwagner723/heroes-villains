from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuperSerializer
from .models import Super

@api_view(['GET', 'POST'])
def supers_list(request):
    if request.method == 'GET':
        supers = Super.objects.all()
        super_types = request.query_params.get('super_type')
        if super_types:
            supers = supers.filter(super_type__type=super_types)
        serializer = SuperSerializer(supers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def supers_and_types(request):
    supers = Super.objects.all()
    heroes = supers.filter(super_type__type='Hero')
    villains = supers.filter(super_type__type='Villain')

    heroes_serializer = SuperSerializer(heroes, many=True)
    villains_serializer = SuperSerializer(villains, many=True)

    custom_response_dict = {
        'Heroes': heroes_serializer.data,
        'Villains': villains_serializer.data
    }
    return Response(custom_response_dict)

@api_view(['GET', 'PUT', 'DELETE'])
def supers_detail(request, pk):
    super = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SuperSerializer(super)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SuperSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SuperTypesSerializer
from super_types.models import SuperTypes

@api_view(['GET'])
def super_types_list(request):
    super_types = SuperTypes.objects.all()
    serializer = SuperTypesSerializer(super_types, many=True)
    return Response(serializer.data)
    
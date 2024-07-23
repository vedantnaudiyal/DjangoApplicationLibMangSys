from .models import BookInstance
import json
from .serializers import BookInstanceSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly


# @api_view(['GET'])
# using function based views to generate CRUD functionality
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated,IsStaffOrReadOnly])
def handleBookInstances(request):
    id = request.GET.get('id')
    if id == None:
        if request.method == 'GET':
            book_instances = BookInstance.objects.all()
            serializer = BookInstanceSerialzer(book_instances, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))

            serializer = BookInstanceSerialzer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    # data=JSONRenderer().render(str(e))
                    return Response(str(e))
            else:
                data = serializer.errors
            return Response(data)
        else:
            return Response("oops Not found", status=404)
    else:
        try:
            book_instance = BookInstance.objects.get(pk=id)
        except Exception as e:
            return Response(str(e))
        if request.method == 'GET':
            serializer = BookInstanceSerialzer(book_instance)
            data = serializer.data
            return Response(data)
        elif request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer = BookInstanceSerialzer(book_instance, data=data, partial=True)

            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    return Response(str(e))
            else:
                data = serializer.errors
            return Response(data)
        elif request.method == 'DELETE':
            try:
                book_instance.delete()
            except Exception as e:
                return Response(str(e))
            res = {
                "msg": f"book_instance with id {id} is successfully deleted"
            }
            # res=JSONRenderer().render(res)
            return Response(res)
        else:
            return Response("oops Not found", status=404)
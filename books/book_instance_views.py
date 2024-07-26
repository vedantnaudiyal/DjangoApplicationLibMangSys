from .models import BookInstance
import json
from .serializers import BookInstanceSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly

from datetime import date

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
                    return Response(str(e), status=400)
            else:
                return Response(serializer.errors, status=400)
            return Response(data, 201)
        else:
            return Response("method not allowed", status=405)
    else:
        try:
            book_instance = BookInstance.objects.get(pk=id)
        except Exception as e:
            return Response(str(e), status=404)
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
                    return Response(str(e), status=400)
            else:
                return Response(serializer.errors, status=400)
            return Response(data)
        elif request.method == 'DELETE':
            try:
                book_instance.delete()
            except Exception as e:
                return Response(str(e), status=404)
            res = {
                "msg": f"book_instance with id {id} is successfully deleted"
            }
            # res=JSONRenderer().render(res)
            return Response(res, status=204)
        else:
            return Response("oops Not found", status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStaffOrReadOnly])
def getBookInstancesByStatus(request):
    status = request.GET.get('status')
    if status == 'a':
        book_instances = BookInstance.objects.filter(status='a')
        serializer = BookInstanceSerialzer(book_instances, many=True)
        return Response(serializer.data)
    elif status == 'b':
        book_instances = BookInstance.objects.filter(status='b')
        serializer = BookInstanceSerialzer(book_instances, many=True)
        return Response(serializer.data)
    elif status == 'n':
        book_instances = BookInstance.objects.filter(status='n')
        serializer = BookInstanceSerialzer(book_instances, many=True)
        return Response(serializer.data)

    return Response(str("please provide a valid book_status"), status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStaffOrReadOnly])
def getBookInstancesLateSubmission(request):

    book_instances = BookInstance.objects.filter(return_date__lt=date.today(), status="b")
    serializer = BookInstanceSerialzer(book_instances, many=True)
    return Response(serializer.data)


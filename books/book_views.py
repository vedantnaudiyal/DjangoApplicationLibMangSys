from .models import Book
import json
from .serializers import BookSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
def handleBooks(request):
    id = request.GET.get('id')
    if id == None:
        if request.method=='GET':
            books = Book.objects.all()
            serializer = BookSerialzer(books, many=True)
            return Response(serializer.data)
        elif request.method=='POST':
            data = json.loads(request.body.decode('utf-8'))
            serializer = BookSerialzer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    # data=JSONRenderer().render(str(e))
                    return Response(str(e), status=400)
            else:
                return Response(serializer.errors, status=400)
            return Response(data)
        else:
            return Response("method not allowed", status=405)
    else:
        try:
            book=Book.objects.get(pk=id)
        except Exception as e:
            return Response(str(e), 404)
        if request.method=='GET':
            serializer = BookSerialzer(book)
            data = serializer.data
            return Response(data)
        elif request.method=='PUT':
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer=BookSerialzer(book, data=data, partial=True)

            if serializer.is_valid():
                try:
                    serializer.save()
                    data=serializer.data
                except Exception as e:
                    return Response(str(e), status=400)
            else:
                return Response(serializer.errors, status=400)
            return Response(data)
        elif request.method=='DELETE':
            try:
                book.delete()
            except Exception as e:
                return Response(str(e), 409)
            res={
                "msg": f"book with id {id} successfully deleted"
            }
            # res=JSONRenderer().render(res)
            return Response(res, 204)
        else:
            return Response("method not allowed", status=405)




@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
def search_by_title(request):
    # data = json.loads(request.body.decode('utf-8'))
    # if data.get(title)
    title = request.GET.get('title')
    if title == None:
        return Response(str("pls specify a title"), 400)
    books = Book.objects.filter(title__contains=title)
    serializer = BookSerialzer(books, many=True)
    return Response(serializer.data)
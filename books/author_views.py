from .models import Author
import json
from .serializers import AuthorSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly


@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def handleAuthors(request):
    id = request.GET.get('id')
    if id == None:
        if request.method == 'GET':
            authors = Author.objects.all()
            serializer = AuthorSerialzer(authors, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            # data=str(request.data)
            # print(type(data))
            # print(str(request.data))

            data = json.loads(request.body.decode('utf-8'))
            serializer = AuthorSerialzer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    # data=JSONRenderer().render(str(e))
                    return Response(str(e), status=400)
            else:
                data = serializer.errors
            return Response(data)
        else:
            return Response("method not allowed", status=405)
    else:
        try:
            author = Author.objects.get(pk=id)
        except Exception as e:
            return Response(str(e), 404)
        if request.method == 'GET':
            serializer = AuthorSerialzer(author)
            data = serializer.data
            return Response(data)
        elif request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer = AuthorSerialzer(author, data=data, partial=True)

            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    return Response(str(e), status=400)
            else:
                return Response(serializer.errors, 400)
            return Response(data)
        elif request.method == 'DELETE':
            print("deleting...")
            try:
                author.delete()
            except Exception as e:
                return Response(str(e), 409)
            res = {
                "msg": f"genre with id {id} successfully deleted"
            }
            return Response(res, 204)
        else:
            return Response("method not allowed", status=405)
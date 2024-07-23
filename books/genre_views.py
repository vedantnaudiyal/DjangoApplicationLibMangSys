from .models import Genre
import json
from .serializers import GenreSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly




# TODO handling put body of unrelated fields
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
def handleGenres(request):
    id = request.GET.get('id')
    if id == None:
        if request.method=='GET':
            genres = Genre.objects.all()
            serializer = GenreSerialzer(genres, many=True)
            return Response(serializer.data)
        elif request.method=='POST':
            data = json.loads(request.body.decode('utf-8'))
            serializer = GenreSerialzer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    return Response(str(e), status=400)
            else:
                data = serializer.errors
            return Response(data)
        else:
            return Response("method not allowed", status=405)
    else:
        try:
            genre=Genre.objects.get(pk=id)
        except Exception as e:
            return Response(str(e), 404)
        if request.method=='GET':
            serializer = GenreSerialzer(genre)
            data = serializer.data
            return Response(data)
        elif request.method=='PUT':
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer=GenreSerialzer(genre, data=data, partial=True)

            if serializer.is_valid():
                try:
                    serializer.save()
                    data=serializer.data
                except Exception as e:
                    return Response(str(e), status=400)
            else:
                return Response(serializer.errors, 400)
            return Response(data)
        elif request.method=='DELETE':
            try:
                genre.delete()
            except Exception as e:
                return Response(str(e), 409)
            res={
                "msg": f"genre with id {id} successfully deleted"
            }
            return Response(res, 204)
        else:
            return Response("method not allowed", status=405)

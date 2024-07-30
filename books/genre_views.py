import logging

from .models import Genre
import json
from .serializers import GenreSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly

logger=logging.getLogger("myapp")


# TODO handling put body of unrelated fields
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
def handleGenres(request):
    id = request.GET.get('id')
    if id == None:
        if request.method=='GET':
            logger.info("fetching all genres!")
            genres = Genre.objects.all()
            serializer = GenreSerialzer(genres, many=True)
            logger.info("successfully fetched all genres!")
            return Response(serializer.data)
        elif request.method=='POST':
            logger.info("adding a genre!")
            data = json.loads(request.body.decode('utf-8'))
            serializer = GenreSerialzer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    logger.error(f"errors: {e}")
                    return Response(str(e), status=400)
            else:
                logger.error(f"errors: {serializer.errors}")
                return Response(serializer.errors, 400)
            logger.info("genre added successfully!")
            return Response(data)
        else:
            logger.info("method not allowed!")
            return Response("method not allowed", status=405)
    else:
        try:
            genre=Genre.objects.get(pk=id)
        except Exception as e:
            logger.error(f"genre with id {id} does not exist!")
            return Response(str(e), 404)
        if request.method=='GET':
            logger.info(f"fetching genre with id {id}!")
            serializer = GenreSerialzer(genre)
            data = serializer.data
            logger.info(f"successfully fetched genre with id {id}!")
            return Response(data)
        elif request.method=='PUT':
            logger.info(f"updating genre with id {id}!")
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer=GenreSerialzer(genre, data=data, partial=True)

            if serializer.is_valid():
                try:
                    serializer.save()
                    data=serializer.data
                except Exception as e:
                    logger.error(f"errors: {e}")
                    return Response(str(e), status=400)
            else:
                logger.error(f"errors: {serializer.errors}")
                return Response(serializer.errors, 400)
            logger.info(f"successfully updated book with id {id}!")
            return Response(data)
        elif request.method=='DELETE':
            logger.info(f"deleting a genre with id {id}!")
            try:
                genre.delete()
            except Exception as e:
                logger.info(f"deletion of genre with id {id} raised errors: {e}!")
                return Response(str(e), 409)
            res={
                "msg": f"genre with id {id} successfully deleted"
            }
            logger.info(f"successfully deleted genre with id {id}!")
            return Response(res, 204)
        else:
            logger.info(f"method not allowed!")
            return Response("method not allowed", status=405)


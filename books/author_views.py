import logging

from .models import Author
import json
from .serializers import AuthorSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly


logger=logging.getLogger("myapp")

@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def handleAuthors(request):
    id = request.GET.get('id')
    if id == None:
        if request.method == 'GET':
            logger.info("fetching all authors!")
            authors = Author.objects.all()
            serializer = AuthorSerialzer(authors, many=True)
            logger.info("successfully fetched all authors!")
            return Response(serializer.data)
        elif request.method == 'POST':
            # data=str(request.data)
            # print(type(data))
            # print(str(request.data))
            logger.info("adding an author!")
            data = json.loads(request.body.decode('utf-8'))

            serializer = AuthorSerialzer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    # data=JSONRenderer().render(str(e))
                    logger.error(f"errors: {e}")
                    return Response(str(e), status=400)
            else:
                logger.error(f"errors: {serializer.errors}")
                return Response(serializer.errors, 400)
            logger.info("author added successfully!")
            return Response(data)
        else:
            logger.info("method not allowed!")
            return Response("method not allowed", status=405)
    else:
        try:
            author = Author.objects.get(pk=id)
        except Exception as e:
            logger.error(f"book with id {id} does not exist!")
            return Response(str(e), 404)
        if request.method == 'GET':
            logger.info(f"fetching author with id {id}!")
            serializer = AuthorSerialzer(author)
            data = serializer.data
            logger.info(f"successfully fetched author with id {id}!")
            return Response(data)
        elif request.method == 'PUT':
            logger.info(f"updating author details with id {id}!")
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer = AuthorSerialzer(author, data=data, partial=True)

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
            logger.info(f"successfully updated author details with id {id}!")
            return Response(data)
        elif request.method == 'DELETE':
            logger.info(f"deleting an author with id {id}!")
            print("deleting...")
            try:
                author.delete()
            except Exception as e:
                logger.info(f"deletion of author with id {id} raised errors: {e}!")
                return Response(str(e), 409)
            res = {
                "msg": f"author with id {id} successfully deleted"
            }
            logger.info(f"successfully deleted author with id {id}!")
            return Response(res, 204)
        else:
            logger.info(f"method not allowed!")
            return Response("method not allowed", status=405)


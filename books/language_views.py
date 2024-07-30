import logging

from .models import Language
import json
from .serializers import LanguageSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly

logger=logging.getLogger("myapp")

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
def handleLanguages(request):
    id = request.GET.get('id')
    if id == None:
        if request.method == 'GET':
            logger.info("fetching all languages!")
            languages = Language.objects.all()
            serializer = LanguageSerialzer(languages, many=True)
            logger.info("successfully fetched all languages!")
            return Response(serializer.data)
        elif request.method == 'POST':
            logger.info("adding a language!")
            data = json.loads(request.body.decode('utf-8'))
            if data.get('name'):
                data['name']=data['name'].lower()
            serializer = LanguageSerialzer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    logger.error(f"errors: {e}")
                    return Response(str(e), status=400)
            else:
                logger.error(f"errors: {serializer.errors}")
                return Response(serializer.errors, status=400)
            logger.info("language added successfully!")
            return Response(data)
        else:
            logger.error("method not allowed!")
            return Response("method not allowed", status=405)
    else:
        try:
            language = Language.objects.get(pk=id)
        except Exception as e:
            logger.error(f"language with id {id} does not exist!")
            return Response(str(e), 404)
        if request.method == 'GET':
            logger.info(f"fetching language with id {id}!")
            serializer = LanguageSerialzer(language)
            data = serializer.data
            logger.info(f"successfully fetched language with id {id}!")
            return Response(data)
        elif request.method == 'PUT':
            logger.info(f"updating language with id {id}!")
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer = LanguageSerialzer(language, data=data, partial=True)

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
            logger.info(f"successfully updated language with id {id}!")
            return Response(data)
        elif request.method == 'DELETE':
            logger.info(f"deleting a language with id {id}!")
            try:
                language.delete()
            except Exception as e:
                logger.error(f"deletion of language with id {id} raised errors: {e}!")
                return Response(str(e), 409)
            res = {
                "msg": f"language with id {id} successfully deleted"
            }
            logger.info(f"successfully deleted language with id {id}!")
            return Response(res, 204)
        else:
            logger.error(f"method not allowed!")
            return Response("oops Not found", status=405)


#
# logger.error(f"errors: {serializer.errors}")
# logger.info("book added successfully!")
# logger.error("method not allowed!")
# logger.error(f"book with id {id} does not exist!")
# logger.info(f"fetching book with id {id}!")
# logger.info(f"successfully fetched book with id {id}!")
# logger.info(f"updating book with id {id}!")
# logger.error(f"errors: {e}")
# logger.error(f"errors: {serializer.errors}")
#
# logger.info(f"successfully updated book with id {id}!")
# logger.info(f"deleting a book with id {id}!")
# logger.error(f"deletion of book with id {id} raised errors: {e}!")
# logger.info(f"successfully deleted book with id {id}!")
# logger.error(f"method not allowed!")
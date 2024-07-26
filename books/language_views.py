from .models import Language
import json
from .serializers import LanguageSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
def handleLanguages(request):
    id = request.GET.get('id')
    if id == None:
        if request.method == 'GET':
            languages = Language.objects.all()
            serializer = LanguageSerialzer(languages, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            if data.get('name'):
                data['name']=data['name'].lower()
            serializer = LanguageSerialzer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    return Response(str(e), status=400)
            else:
                return Response(serializer.errors, status=400)
            return Response(data)
        else:
            return Response("method not allowed", status=405)
    else:
        try:
            language = Language.objects.get(pk=id)
        except Exception as e:
            return Response(str(e), 404)
        if request.method == 'GET':
            serializer = LanguageSerialzer(language)
            data = serializer.data
            return Response(data)
        elif request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer = LanguageSerialzer(language, data=data, partial=True)

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
            try:
                language.delete()
            except Exception as e:
                return Response(str(e), 409)
            res = {
                "msg": f"genre with id {id} successfully deleted"
            }
            return Response(res, 204)
        else:
            return Response("oops Not found", status=405)
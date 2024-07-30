import logging

from .models import BookInstance
import json
from .serializers import BookInstanceSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly

from datetime import date


logger=logging.getLogger("myapp")

# @api_view(['GET'])
# using function based views to generate CRUD functionality
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated,IsStaffOrReadOnly])
def handleBookInstances(request):
    id = request.GET.get('id')
    if id == None:
        if request.method == 'GET':
            logger.info("fetching all book instances!")
            book_instances = BookInstance.objects.all()
            serializer = BookInstanceSerialzer(book_instances, many=True)
            logger.info("successfully fetched all book instances!")
            return Response(serializer.data)
        elif request.method == 'POST':
            logger.info("adding a book instance!")
            data = json.loads(request.body.decode('utf-8'))

            serializer = BookInstanceSerialzer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = serializer.data
                except Exception as e:
                    logger.error(f"errors: {e}")
                    # data=JSONRenderer().render(str(e))
                    return Response(str(e), status=400)
            else:
                logger.error(f"errors: {serializer.errors}")
                return Response(serializer.errors, status=400)
            logger.info("book instance added successfully!")
            return Response(data, 201)
        else:
            logger.error("method not allowed!")
            return Response("method not allowed", status=405)
    else:
        try:
            book_instance = BookInstance.objects.get(pk=id)
        except Exception as e:
            logger.error(f"book instance with id {id} does not exist!")
            return Response(str(e), status=404)
        if request.method == 'GET':
            logger.info(f"fetching book instance with id {id}!")
            serializer = BookInstanceSerialzer(book_instance)
            data = serializer.data
            logger.info(f"successfully fetched book instance with id {id}!")
            return Response(data)
        elif request.method == 'PUT':
            logger.info(f"updating book instance with id {id}!")
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer = BookInstanceSerialzer(book_instance, data=data, partial=True)

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
            logger.info(f"successfully updated book instance with id {id}!")
            return Response(data)
        elif request.method == 'DELETE':
            logger.info(f"deleting a book instance with id {id}!")
            try:
                book_instance.delete()
            except Exception as e:
                logger.error(f"deletion of book instance with id {id} raised errors: {e}!")
                return Response(str(e), status=404)
            res = {
                "msg": f"book_instance with id {id} is successfully deleted"
            }
            # res=JSONRenderer().render(res)
            logger.info(f"successfully deleted book instance with id {id}!")
            return Response(res, status=204)
        else:
            logger.error(f"method not allowed!")
            return Response("oops Not found", status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStaffOrReadOnly])
def getBookInstancesByStatus(request):
    status = request.GET.get('status')
    # if(BookInstance.book_status.index((status in )))
    index=-1
    for ind in range(3):
        if BookInstance.book_status[ind][0]==status:
            index=ind
            break

    if index==-1:
        logger.error(f"no book_instance with status as {status} are available!")
        Response(str("please provide a valid book_status"), status=400)
    logger.info(f"fetching books instances with status {BookInstance.book_status[ind][0]} and are {BookInstance.book_status[ind][1]}")
    if status == 'a':
        book_instances = BookInstance.objects.filter(status='a')
        serializer = BookInstanceSerialzer(book_instances, many=True)
        logger.info(f"{BookInstance.book_status[ind][1]} books are successfully fetched from srever!")
        return Response(serializer.data)
    elif status == 'b':
        book_instances = BookInstance.objects.filter(status='b')
        serializer = BookInstanceSerialzer(book_instances, many=True)
        logger.info(f"{BookInstance.book_status[ind][1]} books are successfully fetched from srever!")
        return Response(serializer.data)
    elif status == 'n':
        book_instances = BookInstance.objects.filter(status='n')
        serializer = BookInstanceSerialzer(book_instances, many=True)
        logger.info(f"{BookInstance.book_status[ind][1]} books are successfully fetched from srever!")
        return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStaffOrReadOnly])
def getBookInstancesLateSubmission(request):
    logger.info("fetching book_instances that are past their due late and their users")
    book_instances = BookInstance.objects.filter(return_date__lt=date.today(), status="b")
    serializer = BookInstanceSerialzer(book_instances, many=True)
    return Response(serializer.data)





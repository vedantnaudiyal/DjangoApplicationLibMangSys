from .models import Book, Author
import json
from .serializers import BookSerialzer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly
import logging

logger = logging.getLogger("myapp")

# def my_view(request):


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
def handleBooks(request):
    id = request.GET.get('id')
    if id == None:
        if request.method=='GET':
            logger.info("fetching all books!")
            books = Book.objects.all()
            serializer = BookSerialzer(books, many=True)
            logger.info("successfully fetched all books!")
            return Response(serializer.data)
        elif request.method=='POST':
            logger.info("adding a book!")
            data = json.loads(request.body.decode('utf-8'))
            serializer = BookSerialzer(data=data)
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
            logger.info("book added successfully!")
            return Response(data)
        else:
            logger.info("method not allowed!")
            return Response("method not allowed", status=405)
    else:
        try:
            book=Book.objects.get(pk=id)
        except Exception as e:
            logger.error(f"book with id {id} does not exist!")
            return Response(str(e), 404)
        if request.method=='GET':
            logger.info(f"fetching book with id {id}!")
            serializer = BookSerialzer(book)
            data = serializer.data
            logger.info(f"successfully fetched book with id {id}!")
            return Response(data)
        elif request.method=='PUT':
            logger.info(f"updating book with id {id}!")
            data = json.loads(request.body.decode('utf-8'))
            # partial true allows to pass few field that is to be updated only
            serializer=BookSerialzer(book, data=data, partial=True)

            if serializer.is_valid():
                try:
                    serializer.save()
                    data=serializer.data
                except Exception as e:
                    logger.error(f"errors: {e}")
                    return Response(str(e), status=400)
            else:
                logger.error(f"errors: {serializer.errors}")
                return Response(serializer.errors, status=400)
            logger.info(f"successfully updated book with id {id}!")
            return Response(data)
        elif request.method=='DELETE':
            logger.info(f"deleting a book with id {id}!")
            try:
                book.delete()
            except Exception as e:
                logger.info(f"deletion of book with id {id} raised errors: {e}!")
                return Response(str(e), 409)
            res={
                "msg": f"book with id {id} successfully deleted"
            }
            # res=JSONRenderer().render(res)
            logger.info(f"successfully deleted book with id {id}!")
            return Response(res, 204)
        else:
            logger.error(f"method not allowed!")
            return Response("method not allowed", status=405)




@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffOrReadOnly])
def search_by_title(request):
    # data = json.loads(request.body.decode('utf-8'))
    # if data.get(title)
    keyword = request.GET.get('keyword')
    if keyword == None:
        return Response(str("pls specify a keyword"), 400)
    books_by_title = Book.objects.filter(title__contains=keyword)
    # author_by_name=Author.objects.filter(name__contains=keyword)
    # # for author in author_by_name:
    #
    # books_by_author = Book.objects.filter(author=4)
    serializer1 = BookSerialzer(books_by_title, many=True)
    # serializer2 = BookSerialzer(books_by_author, many=True)
    return Response({
        "books_by_title": serializer1.data,
        # "books_by_author": serializer2.data,
    })
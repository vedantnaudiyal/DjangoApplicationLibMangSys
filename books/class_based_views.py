from .models import Book
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions

from rest_framework.permissions import IsAuthenticated

from django.views import generic
from rest_framework import generics

from django.contrib.auth.models import User



# ---------------------- class based views (list and detail) ------------------------------

@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class BookListView(generic.ListView):
    model = Book

    paginate_by = 8

    queryset = Book.objects.all()[:5]

    template_name = "books/book_list.html"

@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class BookDetailView(generic.DetailView):
    model = Book

    template_name = "books/book_detail.html"

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):

        serializer=LoginSerializer(data=request.data)
        print("serializer.data")
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(str(e), 400)
        print("hello world!")
        print(serializer.validated_data)
        user=serializer.validated_data.get('username')
        print(user)
        return Response({"username": user}, status=status.HTTP_200_OK)
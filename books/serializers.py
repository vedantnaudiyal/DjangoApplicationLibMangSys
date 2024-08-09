from rest_framework import serializers
from .models import Language, Book, BookInstance, Genre, Author
from django.contrib.auth.models import User

class LanguageSerialzer(serializers.ModelSerializer):
    class Meta:
        model=Language
        fields='__all__'


class BookSerialzer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'


class BookInstanceSerialzer(serializers.ModelSerializer):
    class Meta:
        model=BookInstance
        fields='__all__'


class GenreSerialzer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields='__all__'

    def create(self, validated_data):
        instance=Genre.objects.create(**validated_data)
        return instance


class AuthorSerialzer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # books=serializers.CharField()
    # booksBorrowed=BookInstanceSerialzer(many=True, read_only=True, default=[])
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        fields='__all__'

    def create(self, validated_data):
        password=validated_data.get('password')
        user=self.Meta.model(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user





class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model=User
        fields='__all__'

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise Exception("Must include username and password")

        user=User.objects.filter(username=username).first()

        if user is None:
            raise Exception("Invalid username or password")
        if not user.check_password(password):
            raise Exception("Invalid username or password")

        data['user'] = user
        return data

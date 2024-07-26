from django.db import models
import uuid
from django.urls import reverse
from django.db.models import functions
from django.contrib.auth.models import User

# Create your models here.


class Language(models.Model):
    name=models.CharField(max_length=50, help_text="language in which the book is published(lower_case)", unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("language-detail", args=[str(self.id)])


class  Genre(models.Model):
    name=models.CharField(max_length=50, help_text="Genres for books", unique=True, verbose_name="GenreName")

    class Meta:
        # just for our table since it is small otherwise it is costly
        ordering: ['name']
        constraints=[
            models.UniqueConstraint(
                functions.Lower('name'),
                name="every genre's lowercase name must be unique",
                violation_error_message="Genre already present"
            ),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre-detail", args=[str(self.id)])


class Book(models.Model):
      title=models.CharField(max_length=100, help_text="title for the book" )
      author=models.ForeignKey('Author', on_delete=models.CASCADE, null=True)
      summary=models.TextField(max_length=500, help_text="a small overview of the book!", unique=True, verbose_name="overview")
      ISBN=models.CharField(max_length=13, help_text="ISBN(International Standard Book Number) for the book(13 digits only)", unique=True, verbose_name="ISBN_ID")
      genre=models.ManyToManyField('Genre', help_text="select genre for the book")
      language=models.ForeignKey(Language, models.CASCADE, verbose_name="BookLanguage", help_text="language in which the book is published", null=True)
      def __str__(self):
          return f"{self.title} ISBN {self.ISBN} -by {self.author}"

      def get_absolute_url(self):
          return reverse("book-detail", args=[str(self.id)])

      class Meta:
          # just for our table since it is small otherwise it is costly
          # ordering=['title']
          db_table="book_data"


class BookInstance(models.Model):
    unique_id=models.CharField(max_length=50,help_text="id given to this book instance by library",primary_key=True, default=uuid.uuid4)
    return_date=models.DateField(help_text="When to return?",null=True,blank=True)
    # status=models.enums(['BORROWED', 'RETURNED'])
    book_status=(
        ('a', 'AVAILABLE'),
        ('b', 'BORROWED'),  # can be because this is borrowed by someone already
        ('n', 'NOT_AVAILABLE') # may be because of maintenance
    )
    status=models.CharField(max_length=1, choices=book_status, blank=True, default='a')
    book=models.ForeignKey('Book', on_delete=models.PROTECT)
    issuer = models.ForeignKey(User, on_delete=models.PROTECT, default=3, verbose_name="name of issuer")

    class Meta:
        ordering: ['-return_date']

    def __str__(self):
        return f"{self.unique_id} {self.book.title}"


class Author(models.Model):
    name=models.CharField(max_length=100, help_text="Name of the author", unique=True)
    date_of_birth=models.DateField(help_text="Date of birth", null=True, blank=True)
    date_of_death=models.DateField("Expired",help_text="Date of death", null=True, blank=True)

    def __str__(self):
        return f"author name: {self.name}"

    def get_absolute_url(self):
        return reverse("author_detail", args=[str(self.id)])




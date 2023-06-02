from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Genre(models.Model):
    #Modelo representativo de genero del libro
    name = models.CharField(max_length=200,
    help_text='Introduce genero de libro (e.g. Ciencia ficcion)')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete = models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text = 'Introduce descripcion del libro')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Selecciona genero para este libro')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # Devuelve la URL para acceder a un registro detallado de este libro.
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'


class Language(models.Model):
    name = models.CharField(max_length=200,
    help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name

class BookInstance(models.Model):
    # Modelo que representa una copia específica de un libro 
    #(es decir, que se puede tomar prestado de la biblioteca).
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID único para este libro en particular en toda la biblioteca')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'), #Mantenimiento
        ('o', 'On loan'),     #En carga
        ('a', 'Available'),   #Disponible
        ('r', 'Reserved'),    #Reservado
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        #String para representacion de objeto modelo
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    # Modelo representativo de autor
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        # Devuelve la URL para acceder a una instancia de autor en particular.
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        # Cadena para representar el objeto Modelo.
        return f'{self.last_name}, {self.first_name}'
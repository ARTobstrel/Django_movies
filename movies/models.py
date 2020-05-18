from datetime import date

from django.db import models


# Create your models here.

class Category(models.Model):
    """Category"""
    name = models.CharField("Categoria", max_length=160)
    description = models.TextField("Opisanie")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    """Actors and directors"""
    name = models.CharField("Imya", max_length=160)
    age = models.PositiveSmallIntegerField("Vozrast", default=0)
    description = models.TextField("Opisanie")
    image = models.ImageField("Izobrajenie", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actors and directors"
        verbose_name_plural = "Actors and directors"


class Genre(models.Model):
    """Genres"""
    name = models.CharField("Imya", max_length=160)
    description = models.TextField("Opisanie")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    """Movies"""
    title = models.CharField("Nazvanie", max_length=100)
    tagline = models.CharField("Slogan", max_length=100, default="")
    description = models.TextField("Opisanie")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Date out", default=2020)
    country = models.CharField("Strana", max_length=50)
    directors = models.ManyToManyField(Actor, verbose_name="director", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="actor", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Janri")
    world_premiere = models.DateField("Primiera v mire", default=date.today)
    budget = models.PositiveIntegerField(
        "Budjet", default=0, help_text="summa v baksah"
    )
    fees_in_usa = models.PositiveIntegerField(
        "Sbori v USA", default=0, help_text="summa v baksah"
    )
    fees_in_world = models.PositiveIntegerField(
        "Sbori v USA", default=0, help_text="summa v baksah"
    )
    category = models.ForeignKey(Category, verbose_name="Categoriya", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Chernovik", default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmy"


class MovieShots(models.Model):
    """Shots from film"""
    title = models.CharField('Zagolovok', max_length=100)
    description = models.TextField("Opisanie")
    image = models.ImageField('Izobrajenie', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Film', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Shot from film'
        verbose_name_plural = 'Shots from film'


class RatingStar(models.Model):
    """Zvezda raytinga"""
    value = models.PositiveSmallIntegerField('Znachenie', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Zvezda raytinga"
        verbose_name_plural = "Zvezdi raytinga"


class Rating(models.Model):
    """Rating"""
    ip = models.CharField('IP adress', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='zvezda')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='film')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Rayting'
        verbose_name_plural = 'Raytingi'


class Reviews(models.Model):
    """Otzivi"""
    email = models.EmailField()
    name = models.CharField('Imya', max_length=100)
    text = models.TextField('Text', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Roditel', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='Film', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Otziv'
        verbose_name_plural = 'Otzivi'

from datetime import date

from django.db import models


# Create your models here.
from django.urls import reverse


class Category(models.Model):
    """Category"""
    name = models.CharField("Категория", max_length=160, help_text='название категории')
    description = models.TextField("Описание")
    url = models.SlugField("Поле slug", max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Actors and directors"""
    name = models.CharField("Название", max_length=160)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Фото", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """Genres"""
    name = models.CharField("Название", max_length=160)
    description = models.TextField("Описание")
    url = models.SlugField("Поле slug", max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Movies"""
    title = models.CharField("Название фильма", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default="")
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2020)
    country = models.CharField("Страна", max_length=50)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актёр", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Жанр")
    world_premiere = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveIntegerField(
        "Бюджет", default=0, help_text="сумма в долларах"
    )
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="сумма в долларах"
    )
    fees_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="сумма в долларах"
    )
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Chernovik", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmy"


class MovieShots(models.Model):
    """Shots from film"""
    title = models.CharField('Zagolovok', max_length=100)
    description = models.TextField("Описание")
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
    name = models.CharField('Название', max_length=100)
    text = models.TextField('Текст', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Roditel', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='Film', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Otziv'
        verbose_name_plural = 'Otzivi'

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


# Данный класс позволяет отображать все отзывы к каждому фильму в админке
class ReviewInLine(admin.StackedInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email', 'text', 'movie', 'parent')

class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150px" height="auto">')

    get_image.short_description = "Изображение"


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_display_links = ('title',)
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInLine, ReviewInLine]
    list_editable = ('draft',)
    actions = ["publish", "unpublish"]
    form = MovieAdminForm
    readonly_fields = ('get_image',)
    save_on_top = True
    save_as = True
    fieldsets = (
        ('Название фильма и слоган', {
            'fields': (("title", "tagline"),)
        }),
        ('Описание и постер фильма', {
            'fields': ("description", ("poster", "get_image"))
        }),
        (None, {
            'fields': (("year", "world_premiere", "country"),)
        }),
        ('Актеры, Режиссеры, Жанры и Категорииc', {
            'classes': ('collapse',),
            'fields': (("actors", "directors", "genres", "category"),)
        }),
        ('Бюджет, сборы в США и в мире', {
            'fields': (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        (None, {
            'fields': (("url", "draft"),)
        }),
    )

    # Метод позволяет выводить изображение в админку
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="150px" height="auto">')

    # Пишем свои экшены в админке
    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 row was updated'
        else:
            message_bit = f'{row_update} rows was updated'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 row was updated'
        else:
            message_bit = f'{row_update} rows was updated'
        self.message_user(request, f'{message_bit}')

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Изображение"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email', 'text', 'movie', 'parent')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'description', 'get_image', 'id')
    list_display_links = ('name',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80px" height="auto">')

    get_image.short_description = "Изображение"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_display_links = ('name',)


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'get_image', 'movie', 'id')
    list_display_links = ('title',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150px" height="auto">')

    get_image.short_description = "Изображение"


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)
    list_display_links = ('value',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'star', 'movie')
    list_display_links = ('ip',)

# Можно так
# admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Административная панель'
admin.site.site_header = 'Административная панель'

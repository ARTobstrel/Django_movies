from django.urls import path

from .views import MoviesView, MovieDetailView, AddReview

urlpatterns = [
    path('', MoviesView.as_view(), name='movies'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
]

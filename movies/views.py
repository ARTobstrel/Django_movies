from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from movies.models import Movie
from .forms import ReviewForm

class MoviesView(ListView):
    """List movies"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
    """Detail View"""
    model = Movie
    slug_field = "url"

class AddReview(View):
    """Reviews"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())

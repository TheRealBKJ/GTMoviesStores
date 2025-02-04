from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Movie, Review


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
def add_review(request, movie_id):
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=movie_id)
        Review.objects.create(
            movie=movie,
            user=request.user,
            rating=request.POST['rating'],
            comment=request.POST['comment']
        )
        return redirect('movie_detail', movie_id=movie_id)
    return redirect('movie_list')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movie_detail', movie_id=review.movie.id)


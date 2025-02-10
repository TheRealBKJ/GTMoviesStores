from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, Review
# Create your views here.

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})


def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie).order_by('-date')

    template_data = {
        'movie': movie,
        'reviews': reviews
    }

    return render(request, 'movies/show.html', {'template_data': template_data})


@login_required
def create_review(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        if comment:  # Ensure the comment is not empty
            review = Review.objects.create(
                comment=comment,
                movie=movie,
                user=request.user
            )
            review.save()

    return redirect('movies.show', id=id)

def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {
            'title': 'Edit Review',
            'review': review
        }
        return render(request, 'movies/edit_review.html', {'template_data': template_data})

    elif request.method == 'POST' and request.POST.get('comment', '') != '':
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)

    return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user == review.user or request.user.is_superuser:
        review.delete()

    return redirect('movies.show', id=id)




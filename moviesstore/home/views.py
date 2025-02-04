from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home/index.html') #returns html page when http request to website
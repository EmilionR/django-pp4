from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def base_board(request):
    return HttpResponse("Hello, World!")
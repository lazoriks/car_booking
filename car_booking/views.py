from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')

def booking(request):
    return render(request, 'booking/booking.html')

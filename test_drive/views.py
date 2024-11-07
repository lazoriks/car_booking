from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from .forms import BookingForm, RequestToBuyForm
from .models import Booking, RequestToBuy

@login_required
def create_booking_and_request(request):
    booking_form = BookingForm()
    request_form = RequestToBuyForm()

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        request_form = RequestToBuyForm(request.POST)

        if booking_form.is_valid() and request_form.is_valid():
            booking = booking_form.save(commit=False)
            request_to_buy = request_form.save(commit=False)
            booking.user = request.user
            request_to_buy.user = request.user
            booking.save()
            request_to_buy.save()
            messages.success(request, 'Your booking and request to buy have been submitted.')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'booking/booking.html', {
        'booking_form': booking_form,
        'request_form': request_form,
    })

def report_view(request):
    bookings = Booking.objects.all()
    requests_to_buy = RequestToBuy.objects.all()

    return render(request, 'booking/report.html', {
        'bookings': bookings,
        'requests_to_buy': requests_to_buy,
    })

def login_or_register(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        register_form = UserCreationForm(data=request.POST)

        if 'login' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('booking')

        elif 'register' in request.POST:
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('booking')
            else:
                messages.error(request, "Registration failed. Please correct the errors below.")

    else:
        login_form = AuthenticationForm()
        register_form = UserCreationForm()

    return render(request, 'registration/login.html', {
        'login_form': login_form,
        'register_form': register_form
    })

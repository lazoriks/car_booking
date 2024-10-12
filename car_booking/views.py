from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import Booking
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from django.http import HttpResponseNotFound
from django.template import loader
#from django.views.decorators.csrf import requires_csrf_token
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
def custom_404(request, exception):
    template = loader.get_template('404.html')
    return HttpResponseNotFound(template.render())

@csrf_exempt
def booking(request):
    today = datetime.now()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Отримуємо бронювання (якщо користувач авторизований)
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(date__range=[first_day_of_month, last_day_of_month], user=request.user)
    else:
        bookings = Booking.objects.filter(date__range=[first_day_of_month, last_day_of_month])

    reserved_dates = {booking.date.date(): booking.id for booking in bookings}
    calendar_days = []

    for day in range(1, last_day_of_month.day + 1):
        date = first_day_of_month.replace(day=day)
        is_reserved = date.date() in reserved_dates

        # Для неавторизованих користувачів:
        editable = request.user.is_authenticated and (is_reserved and (reserved_dates[date.date()] in bookings.values_list('id', flat=True)))

        calendar_days.append({
            'day_number': day,
            'date': date.strftime('%Y-%m-%d'),
            'is_reserved': is_reserved,
            'editable': editable,
            'booking_id': reserved_dates.get(date.date(), None)
        })

    # Завжди повертаємо JSON для AJAX-запитів, незалежно від наявності бронювань
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(calendar_days, safe=False)  # Завжди повертаємо JSON для AJAX-запитів

        # Якщо це звичайний запит, повертаємо сторінку
    return render(request, 'booking/booking.html', {'calendar_days': calendar_days})

@csrf_exempt
@login_required
def store_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('bookingId')
        date = request.POST.get('date')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        mobile = request.POST.get('mobile')
        email = request.POST['email']

        if booking_id:
            booking = Booking.objects.get(id=booking_id)
            booking.name = name
            booking.surname = surname
            booking.mobile = mobile
            booking.email = email
            booking.save()
        else:
            Booking.objects.create(user=request.user, date=date, name=name, surname=surname, mobile=mobile, email=email)

        send_booking_confirmation(email, date, "Car Information Here")

    return JsonResponse({'status': 'success'})

def send_booking_confirmation(email, date, car_info):
    subject = 'Booking Confirmation for Test Drive'
    message = f'Your test drive is booked for {date}. \n\nCar Information: {car_info}'
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [email])

@login_required
def get_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return JsonResponse({
        'name': booking.name,
        'surname': booking.surname,
        'mobile': booking.mobile
    })

@login_required
def delete_booking(request, booking_id):
    if request.method == 'DELETE':
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)
def index(request):
    return render(request, 'home/index.html')

def booking(request):
    return render(request, 'booking/booking.html')
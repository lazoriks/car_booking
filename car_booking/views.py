from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from django.contrib import messages

from django.http import HttpResponseNotFound
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from car_booking.forms import SubscriptionForm
from car_booking.models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


def donate(request):
    if request.method == 'POST':
        amount = int(request.POST['amount']) * 100
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Website Donation',
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/donate/'),
            )
            return redirect(session.url, code=303)
        except Exception as e:
            return render(request, 'booking/donate.html', {'error': str(e)})
    return render(request, 'booking/donate.html')


def success(request):
    return render(request, 'booking/success.html')


@csrf_exempt
def custom_404(request, exception):
    template = loader.get_template('404.html')
    return HttpResponseNotFound(template.render())


def index(request):
    return render(request, 'home/index.html')


def booking(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('booking')
    else:
        form = AuthenticationForm()

    return render(request, 'booking/booking.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['subscribed_email'] = email
            messages.success(request, f'''
You have successfully subscribed to the newsletter!
''')
            return redirect('index')
        else:
            messages.error(request, f'''
There was an error with your subscription.
''')
    else:
        form = SubscriptionForm()

    return render(request, 'home/subscribe.html', {'form': form})

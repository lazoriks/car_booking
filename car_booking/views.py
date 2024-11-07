from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseNotFound
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


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

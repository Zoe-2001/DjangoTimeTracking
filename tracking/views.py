from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone,formats

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib.auth.models import User

from tracking.form import LoginForm, RegisterForm
from tracking.models import TimeEntry, TotalTime

from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
import json
from django.db.models import Count, Sum, F
import datetime

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'tracking/login.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'tracking/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('mainpage'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'tracking/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.f
    if not form.is_valid():
        return render(request, 'tracking/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('mainpage'))



def login_check(request):
    if not request.user.is_authenticated or not request.user or not request.user.id:
        return False
    return True

def _my_json_error_response(message, status=200):
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)


@login_required
def mainpage_action(request):
    if request.method == 'GET':
        user = request.user
        last_entry = TimeEntry.objects.filter(user=user).order_by('-start_time').first()
        has_started = last_entry and last_entry.end_time is None

        total_working_time_timedelta = TimeEntry.objects.filter(user=user, end_time__isnull=False).aggregate(
            total_time=Sum(F('end_time') - F('start_time')))['total_time'] or datetime.timedelta(seconds=0)
        total_working_time_seconds = total_working_time_timedelta.total_seconds()
        hours, remainder = divmod(total_working_time_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_working_time_formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

        hourly_rate = 80
        accumulated_salary = (total_working_time_seconds / 3600) * hourly_rate

        context = {
            'has_started': has_started,
            'total_working_time': total_working_time_formatted,
            'accumulated_salary': accumulated_salary,
        }

        return render(request, 'tracking/mainpage.html', context)

@login_required
def start_work(request):
    if request.method == 'POST':
        TimeEntry.objects.create(user=request.user, start_time=timezone.now())

    return redirect('mainpage')

@login_required
def end_work(request):
    if request.method == 'POST':
        entry = TimeEntry.objects.filter(user=request.user, end_time__isnull=True).order_by('-start_time').first()
        if entry:
            entry.end_time = timezone.now()
            entry.save()

    return redirect('mainpage')

@login_required
def total_working_time(self):
    entries = TimeEntry.objects.filter(user=self)
    total_time = sum((entry.end_time - entry.start_time).total_seconds() for entry in entries if entry.end_time)
    return total_time
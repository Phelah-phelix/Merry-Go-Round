from django.db import DatabaseError
from django.db.utils import OperationalError, ProgrammingError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PickedNumber
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

NUMBER_LIMIT = 10


def initialize_numbers():
    try:
        PickedNumber.objects.filter(number__gt=NUMBER_LIMIT).delete()
        for i in range(1, NUMBER_LIMIT + 1):
            PickedNumber.objects.get_or_create(number=i)
    except (DatabaseError, OperationalError, ProgrammingError):
        return


def home(request):
    initialize_numbers()
    return render(request, 'picker/home.html')


@csrf_exempt
def pick_number(request):
    if request.method == 'POST':
        user = request.POST.get('user', '').strip()
        if not user:
            return JsonResponse({'error': 'Please enter your name'}, status=400)

        available_numbers = PickedNumber.objects.filter(is_picked=False)
        if available_numbers.exists():
            random_number = random.choice(available_numbers)
            random_number.user = user
            random_number.is_picked = True
            random_number.save()
            return JsonResponse({
                'number': random_number.number,
                'user': user
            })
        return JsonResponse({'error': 'No numbers left'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def results(request):
    picked_numbers = PickedNumber.objects.filter(is_picked=True)
    return render(request, 'picker/results.html', {'picked_numbers': picked_numbers})


def clear_results(request):
    if request.method == 'POST':
        user = request.POST.get('user', '').strip()
        if not user:
            messages.error(request, 'Please enter your name to clear your result.')
            return redirect('results')

        cleared = PickedNumber.objects.filter(user=user)
        cleared_count = cleared.count()
        cleared.update(is_picked=False, user=None, is_saved=False)
        messages.success(request, f'Cleared {cleared_count} result(s) for {user}.')
        return redirect('results')

    messages.error(request, 'Please enter your name to clear your result.')
    return redirect('results')


def save_results(request):
    saved_count = PickedNumber.objects.filter(is_picked=True).count()
    PickedNumber.objects.filter(is_picked=True).update(is_saved=True)
    messages.success(request, f'Saved {saved_count} results!')
    return redirect('results')
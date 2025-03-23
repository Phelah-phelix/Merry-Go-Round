import logging
from django.shortcuts import render
from django.http import JsonResponse
from .models import PickedNumber
import random

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'picker/home.html')

def pick_number(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        logger.info(f"Received user: {user}")
        if not user:
            return JsonResponse({'error': 'User name is required'}, status=400)

        available_numbers = PickedNumber.objects.filter(is_picked=False)
        if available_numbers.exists():
            random_number = random.choice(available_numbers)
            random_number.user = user
            random_number.is_picked = True
            random_number.save()
            return JsonResponse({'number': random_number.number, 'user': user})
        else:
            return JsonResponse({'error': 'No numbers left'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def results(request):
    picked_numbers = PickedNumber.objects.filter(is_picked=True)
    return render(request, 'picker/results.html', {'picked_numbers': picked_numbers})
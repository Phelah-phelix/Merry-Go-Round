from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PickedNumber
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def clear_results(request):
    cleared_count = PickedNumber.objects.filter(is_picked=True, is_saved=False).count()
    PickedNumber.objects.filter(is_picked=True, is_saved=False).delete()
    PickedNumber.objects.all().update(is_picked=False, user=None)
    messages.success(request, f'Cleared {cleared_count} unsaved results!')
    return redirect('results')

def save_results(request):
    saved_count = PickedNumber.objects.filter(is_picked=True, is_saved=False).count()
    PickedNumber.objects.filter(is_picked=True).update(is_saved=True)
    messages.success(request, f'Saved {saved_count} results!')
    return redirect('results')

def initialize_numbers():
    # Create numbers 1-13 if they don't exist
    for i in range(1, 14):
        PickedNumber.objects.get_or_create(number=i)

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
    # Clear only unsaved results
    PickedNumber.objects.filter(is_picked=True, is_saved=False).delete()
    # Reset remaining numbers
    PickedNumber.objects.all().update(is_picked=False, user=None)
    return redirect('results')

def save_results(request):
    # Mark current results as saved
    PickedNumber.objects.filter(is_picked=True).update(is_saved=True)
    return redirect('results')
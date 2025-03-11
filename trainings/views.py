from django.shortcuts import render
from .models import Training  # Sigurohu që ky model ekziston

def training_list(request):
    """Shfaq listën e trajnimeve"""
    trainings = Training.objects.all()
    return render(request, 'trainings/training_list.html', {'trainings': trainings})

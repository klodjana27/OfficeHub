from django.shortcuts import render

def notifications_view(request):
    """Shfaq listën e njoftimeve"""
    return render(request, 'notifications/notifications.html')

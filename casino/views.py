from django.shortcuts import render

def casino_home(request):
    return render(request, 'casino/casino.html')

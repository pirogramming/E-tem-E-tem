from django.shortcuts import render

def loginhome(request):
    return render(request, 'login/loginhome.html')

from django.shortcuts import render

def _404(request):
    context = {}
    return render(request, 'html/404.html', context)
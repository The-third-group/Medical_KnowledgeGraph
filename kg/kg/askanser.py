from django.shortcuts import render
def ask(request):
    context = {}
    return render(request, 'html/askanser.html', context)
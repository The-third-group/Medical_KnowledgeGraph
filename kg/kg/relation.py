from django.shortcuts import render

def rel(request):
    context ={}
    return render(request, 'Relationship between.html', context)
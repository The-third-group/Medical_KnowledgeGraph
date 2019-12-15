from django.shortcuts import render
from model.neo_model import Neo4j
def new_index(request):
    n = Neo4j()
    n.connectDB()
    context ={}
    return render(request, 'index.html', context)
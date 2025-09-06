from django.shortcuts import render

from material.models import Material

# Create your views here.

def material(request):
    materials = Material.objects.all()

    return render(request, 'material/material.html', {'materials': materials})
from django.shortcuts import render, redirect

from material.models import Material

# Create your views here.

def material(request):
    materials = Material.objects.all()

    return render(request, 'material/material.html', {'materials': materials})

def add_material(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        image = request.FILES.get('image')
        yt_url = request.POST.get('yt_url')
        creator = request.user
        if file or image or yt_url:
            Material.objects.create(name=name, description=description, file=file, image=image, yt_url=yt_url, creator=creator)
        else:
            return render(request, 'material/add_material.html', {'error': 'Будь ласка, додайте файл, зображення або URL відео.'})
        return redirect('material')
    return render(request, 'material/add_material.html')

def delet_material(request, material_id):
    material = Material.objects.get(id=material_id)
    if request.method == 'POST':
        material.delete()
        return redirect('material')
    return render(request, 'material/delet_material.html', {'material': material})
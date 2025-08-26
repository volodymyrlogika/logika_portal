from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GalleryItem
from .forms import GalleryItemForm

def gallery_list(request):
    items = GalleryItem.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'gallery/gallery_list.html', {'items': items})

@login_required
def gallery_upload(request):
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.uploaded_by = request.user
            item.status = 'pending'
            item.save()
            return redirect('gallery_list')
    else:
        form = GalleryItemForm()
    return render(request, 'gallery/gallery_upload.html', {'form': form})

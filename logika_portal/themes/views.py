from django.shortcuts import render, redirect, get_object_or_404
from .forms import ThemeForm
from logika_portal.themes.models import Theme



def theme_list(request):
    themes = Theme.objects.all()
    return render(request, 'themes/theme_list.html', {'themes': themes})

def theme_create(request):
    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('theme_list')
    else:
        form = ThemeForm()
    return render(request, 'themes/theme_form.html', {'form': form})

def theme_delete(request, pk):
    theme = get_object_or_404(Theme, pk=pk)
    if request.method == 'POST':
        theme.delete()
        return redirect('theme_list')
    return render(request, 'themes/theme_confirm_delete.html', {'theme': theme})

def test_theme(request):
    return render(request, 'themes/test_theme.html')

from django.shortcuts import redirect, render
from .models import Portfolio
from .forms import PortfolioForm

def PortfolioCreated(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            Portfolio = form.save(commit=False)
            if request.user.is_authenticated:
                 Portfolio.autor = request.user
            Portfolio.save()
            return redirect('portfolio_list')
    else:
         form = PortfolioForm()
    return render(request, 'portfolio/portfolio_form.html', {'form': form})

def PortfolioListView(request):
    portfolio = Portfolio.objects.all()
    return render(request, 'portfolio/portfolio_list.html', {'portfolio': portfolio})


# Create your views here.

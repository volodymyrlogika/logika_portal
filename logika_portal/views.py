from django.shortcuts import render


def main_view(request):
    return render(request, "main.html")


def workshop_view(request):
    return render(request, "workshop/workshop.html")


def theme_creator_view(request):
    return render(request, "themes/themes_create.html")


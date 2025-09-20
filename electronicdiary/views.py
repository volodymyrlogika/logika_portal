from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def grades_list(request):
    grades = [
        {"student_name": "", "subject": "Математика", "score": 11, "date": "2025-09-19"},
        {"student_name": "", "subject": "Фізика", "score": 12, "date": "2025-09-18"},
    ]
    return render(request, 'list.html', {'grades': grades})




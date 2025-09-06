from django.shortcuts import render

from lesson.models import Lesson

def room_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, template_name="room_list.html", context=context)
def Lesson(request,id_room):
    Lessons = get_object_or_404(Lesson,id = id_room)
    context = {
        'room': room_list
    }
    return render(request, template_name='booking.html',context=context)

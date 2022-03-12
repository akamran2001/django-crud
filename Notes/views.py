from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Message
# Create your views here.


@csrf_exempt
def index(request):
    if request.method == "POST":
        title = request.POST.dict()['title']
        desc = request.POST.dict()['description']
        Message.objects.create(title=title, text=desc)
    if request.method == "DELETE":
        item_id = request.body
        Message.objects.filter(id=item_id).delete()

    return render(request, 'Notes/index.html', context={'message': 'Shwmae, byd!', 'messages': Message.objects.all()})


def edit(request):

    if request.method == "POST":
        query = request.POST.dict()
        note_id = query['note_id']
        title = query['title']
        desc = query['description']
        obj = Message.objects.filter(id=note_id)[0]
        obj.title = title
        obj.text = desc
        obj.save()

    if request.method == "GET":
        query = request.GET.dict()
        if 'note' in query:
            note_id = query['note']
            title = Message.objects.filter(id=note_id)[0].title
            desc = Message.objects.filter(id=note_id)[0].text
            return render(request, 'Notes/edit.html', context={'message': 'Shwmae, byd!', 'title': title, "desc": desc, "note_id": note_id})

    return redirect('index')


def notes(request, id):
    return render(request, 'Notes/note.html', context={"message": Message.objects.filter(id=id)[0]})

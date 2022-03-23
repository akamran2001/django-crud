from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Message


def index(request):
    if request.method == "POST":
        files = request.FILES.dict()
        req = request.POST.dict()
        title = req['title']
        desc = req['description']
        m = 0
        if 'image' in files:
            m = Message.objects.create(title=title, text=desc, image=files['image'])
        else:
            m = Message.objects.create(title=title, text=desc)
        return redirect(F"{request._get_scheme()}://{request.get_host()}/notes/{m.id}/")
    return render(request, 'Notes/index.html', context={'header': 'Django Notes', 'messages': Message.objects.all()})


def edit(request):
    if request.method == "POST":
        files = request.FILES.dict()
        req = request.POST.dict()
        note_id = req['note_id']
        title = req['title']
        desc = req['description']
        obj = Message.objects.filter(id=note_id)[0]
        obj.title = title
        obj.text = desc
        if 'image' in files:
            obj.image.delete()
            obj.image = files['image']
        obj.save()
        return redirect('notes', id=note_id)
    else:
        # Get Request
        req = request.GET.dict()
        if 'note' in req:
            note_id = req['note']
            note = ""
            note = Message.objects.filter(id=note_id)[0]
            title = note.title
            desc = note.text
            note_link = F"{request._get_scheme()}://{request.get_host()}/notes/{note_id}/"
            context = {
                'header': 'Django Notes',
                'title': title,
                "desc": desc,
                "note_id": note_id,
                "note_link": note_link
            }
            return render(request, 'Notes/edit.html', context=context)
        else:
            return redirect('index')


def notes(request, id=None):
    if(id):
        note = Message.objects.filter(id=id)[0]
        if request.method == "DELETE":
            if note.image:
                note.image.delete()
            note.delete()
            return redirect('index')
        else:
            context = {
                "title": note.title,
                "lines": note.text.split("\n"),
                "edit_link": F"{request._get_scheme()}://{request.get_host()}/edit/?note={id}",
                "img_link": "#" if not note.image else note.image.url
            }
            return render(request, 'Notes/note.html', context=context)
    else:
        return redirect('index')

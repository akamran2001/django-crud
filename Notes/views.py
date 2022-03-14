from django.shortcuts import redirect, render
from .models import Message


def index(request):
    if request.method == "POST":
        files = request.FILES.dict()
        title = request.POST.dict()['title']
        desc = request.POST.dict()['description']
        if 'image' in files:
            Message.objects.create(title=title, text=desc, image=files['image'])
        else:
            Message.objects.create(title=title, text=desc)
    return render(request, 'Notes/index.html', context={'header': 'Django Notes', 'messages': Message.objects.all()})


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
            note_link = F"{request._get_scheme()}://{request.get_host()}/notes/{note_id}/"
            context = {
                'header': 'Django Notes',
                'title': title,
                "desc": desc,
                "note_id": note_id,
                "note_link": note_link
            }
            return render(request, 'Notes/edit.html', context=context)

    return redirect('index')


def notes(request, id=None):
    if(id):
        try:
            note = Message.objects.filter(id=id)[0]
        except IndexError:
            return redirect("index")
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
        return redirect("index")

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Message
# Create your views here.


@csrf_exempt
def index(request):
    if request.method == "POST":
        entry = request.POST.dict()['entry']
        Message.objects.create(text=entry)
    if request.method == "DELETE":
        item_id = request.body
        Message.objects.filter(id=item_id).delete()

    return render(request, 'Notes/index.html', context={'message': 'Shwmae, byd!', 'messages': Message.objects.all()})


def edit(request):

    if request.method == "POST":
        query = request.POST.dict()
        note_id = query['note_id']
        entry = query['entry']
        obj = Message.objects.filter(id=note_id)[0]
        obj.text = entry
        obj.save()

    if request.method == "GET":
        query = request.GET.dict()
        if 'note' in query:
            note_id = query['note']
            note = Message.objects.filter(id=note_id)[0].text
            return render(request, 'Notes/edit.html', context={'message': 'Shwmae, byd!', 'note': note, "note_id": note_id})

    return redirect('index')

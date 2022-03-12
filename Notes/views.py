from django.shortcuts import render
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

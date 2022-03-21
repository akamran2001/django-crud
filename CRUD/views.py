from django.shortcuts import render


def handle_404(request, exception):
    return render(request, '404.html', status=404)


def handle_403(request, exception):
    return render(request, '403.html', status=403)


def handle_500(request):
    return render(request, '500.html', status=500)

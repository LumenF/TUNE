from django.shortcuts import render


def server_error(request):
    return render(request, 'html/500.html', {})



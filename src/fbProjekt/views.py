from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def main_view(request):
    user = request.user
    test_text = 'Test text!'


    context = {
        'user': user,
        'test_text': test_text,
    }
    return render(request, 'main/index.html', context)

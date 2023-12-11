from django.shortcuts import render


def home(incoming):
    return render(incoming, 'home.html')
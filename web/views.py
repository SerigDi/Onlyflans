from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Flan, ContactForm
#from .forms import ContactFormForm
from .forms import ContactFormModelForm as ContactFormForm


def index(request):
    flanes = Flan.objects.filter(is_private=False)
    return render(request, 'index.html', {'flanes': flanes})


def about(request):
    return render(request, 'about.html')


@login_required
def welcome(request):
    flanes = Flan.objects.filter(is_private=True)
    return render(request, 'welcome.html', {'flanes': flanes})


def contacto(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            ContactForm.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/exito')
    else:
        form = ContactFormForm()

    return render(request, 'contactus.html', {'form': form})


def exito(request):
    return render(request, 'exito.html')


# Mejora Hito 4: vista de detalle para un Flan especifico, usando su slug
def flan_detalle(request, slug):
    flan = get_object_or_404(Flan, slug=slug)
    return render(request, 'flan_detalle.html', {'flan': flan})

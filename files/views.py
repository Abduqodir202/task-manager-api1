from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from files.form import DocumentForm
from files.models import Document


def files_list(request):
    files = Document.objects.all()
    return render(request, 'files/list.html', {'files': files})


def files_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('files_list')
        return render(request, 'files/create.html', {'form': form})
    else:
        form = DocumentForm()
        return render(request, 'files/create.html', {'form': form})


def files_update(request, pk=None):
    file = Document.objects.filter(id=pk).first()

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            return redirect('files_list')
        return render(request, 'files/update.html', {'form': form})
    else:

        form = DocumentForm(instance=file)
        return render(request, 'files/update.html', {'form': form})

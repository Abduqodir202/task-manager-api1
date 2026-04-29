from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from transactions.forms import TransactionForm


def create_transactions(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
        return render(request, 'transaction/create.html', {'form': form})
    else:
        form = TransactionForm()
        return render(request, 'transaction/create.html', {'form': form})

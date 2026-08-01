from django import forms
from django.db import transaction

from transactions.models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['from_user', 'to_user', 'amount']

    @transaction.atomic
    def save(self, commit=True):
        from_user = self.cleaned_data['from_user']
        to_user = self.cleaned_data['to_user']
        amount = self.cleaned_data['amount']

        to_user.amount += amount
        to_user.save()

        from_user.amount -= amount
        from_user.save()

        if from_user == to_user:
            raise forms.ValidationError("You cannot add money to the same user")

        if from_user.amount < amount:
            raise forms.ValidationError("Sizda yetarli mablag mavjud emas")

        return Transaction.objects.create(from_user=from_user, to_user=to_user, amount=amount)

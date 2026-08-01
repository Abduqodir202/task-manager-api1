from tabnanny import verbose

from django import forms

from books.models import Books


class BooksForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea,
                                  label="Xabar")
    price = forms.DecimalField(max_digits=10, decimal_places=2)


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title_uz', 'title_en', 'title_ru', 'description_uz','description_en','description_ru', 'price', 'authors']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your description',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'authors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("5 ta harfdan koproq kirit")
        return title

    # def clean(self):
    #     title = self.cleaned_data['title']
    #     description = self.cleaned_data['description']
    #
    #     if title == description:
    #         raise forms.ValidationError("title va descriptionga bir xil malumot mumkin emas")
    #     return self.cleaned_data

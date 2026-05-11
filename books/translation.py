from modeltranslation.translator import register, TranslationOptions
from books.models import Books


@register(Books)
class BookTranslationOptions(TranslationOptions):
    # Bu maydonlar har bir tilga tarjima qilinadi
    fields = ('title', 'description')

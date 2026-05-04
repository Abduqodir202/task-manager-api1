from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from accounts.models import UserRole
from books.forms import BookModelForm
from books.models import Books, Status


def book_list(request):
    search = request.GET.get('search', '')
    page = request.GET.get('page')
    books = Books.objects.all()  # Queryset list [<booq1>.
    if request.user.is_authenticated and request.user.role == UserRole.POSTER:
        books = books.filter(created_by=request.user)
    elif request.user.is_authenticated and request.user.role == UserRole.MODERATOR:
        books = books.filter(status=Status.DRAFT)
    else:
        books = books.filter(status=Status.PUBLISHED)
    if search:
        books = books.filter(Q(title__icontains=search) | Q(description__icontains=search))
    paginator = Paginator(books, 3)
    books = paginator.get_page(page)
    return render(request, 'books/list.html', {"books": books, 'search': search})


class BookListView(ListView):
    model = Books
    template_name = 'books/list.html'
    context_object_name = 'books'
    queryset = Books.objects.all()
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['search'] = \
            self.request.GET.get('search', '')
        return context

    def get_queryset(self):
        search = self.request.GET.get('search', '')

        if self.request.user.is_authenticated and self.request.user.role == UserRole.POSTER:
            books = self.queryset.filter(created_by=self.request.user)
        elif self.request.user.is_authenticated and self.request.user.role == UserRole.MODERATOR:
            books = self.queryset.filter(status=Status.DRAFT)
        else:
            books = self.queryset.filter(status=Status.PUBLISHED)

        if search:
            books = books.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return books


class BooksCreateView(PermissionRequiredMixin, CreateView):
    model = Books
    template_name = 'books/create.html'
    form_class = BookModelForm
    success_url = reverse_lazy('book_list')
    permission_required = 'books.add_books'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BooksUpdateView(PermissionRequiredMixin, UpdateView):
    model = Books
    template_name = 'books/update.html'
    form_class = BookModelForm
    permission_required = 'books.change_books'
    success_url = reverse_lazy('book_list')
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BooksDeleteView(PermissionRequiredMixin, DeleteView):
    model = Books
    success_url = reverse_lazy('book_list')
    permission_required = 'books.delete_books'
    pk_url_kwarg = 'pk'
    template_name = 'books/delete.html'


def book_detail(request, pk):
    book = Books.objects.filter(id=pk).first()
    return render(request, 'books/detail.html', {"book": book})


# @login_required
# @is_poster
@permission_required('books.add_books', raise_exception=True)
def book_create_form(request):
    # form = BooksForm()
    form = BookModelForm()
    return render(request, 'books/create.html', {"form": form})


# @login_required
# @is_poster
@permission_required('books.add_books', raise_exception=True)
def book_create(request):
    # data = request.POST
    # book = Books(title=data.get("title"), description=data.get("description"), price=data.get("price"))
    # book.save()
    # # Books.objects.create(title=data['title'], description=data['description'], price=data['price'])
    # return redirect('book_list')
    # form = BooksForm(request.POST)
    form = BookModelForm(request.POST)
    if form.is_valid():
        # data = form.cleaned_data
        # Books.objects.create(**data)
        book = form.save(commit=False)
        book.created_by = request.user
        book.save()
        return redirect('book_list')
    return render(request, 'books/create.html', {"form": form})


# @login_required
# @is_poster
@permission_required('books.change_books', raise_exception=True)
def book_update_forme(request, pk=None):
    book = Books.objects.filter(id=pk).first()
    form = BookModelForm(instance=book)
    return render(request, 'books/update.html', {"form": form, "book": book})


# @login_required
# @is_poster
@permission_required('books.change_books', raise_exception=True)
def book_update(request, pk=None):
    # Books.objects.filter(id=pk).update(title=request.POST.get("title"), description=request.POST.get("description"),
    #                                    price=request.POST.get("price"))
    book = Books.objects.filter(id=pk).first()
    form = BookModelForm(instance=book, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/update.html', {"form": form, "book": book})


# @login_required_custom
# @is_poster
@permission_required('books.delete_books', raise_exception=True)
def book_delete(request, pk=None):
    b1 = Books.objects.filter(id=pk).first()
    b1.delete()
    return redirect('book_list')


# @is_moderator
@permission_required('books.can_publish', raise_exception=True)
def book_published(request, pk=None):
    book = Books.objects.filter(id=pk).first()
    book.status = Status.PUBLISHED
    book.save()
    return redirect('book_list')

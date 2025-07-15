from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book
from .forms import BookForm,ProfileForm, CustomUserChangeForm, UserForm
from project.models import Profile


@login_required
def home(request):
    context = {

    }
    return render(request, 'project/home.html', context=context)


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'user/register.html', {'form': form})


@login_required
def log_out(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    user = request.user
    profile_ = Profile.objects.filter(user=user).first()
    context = {
        'profile': profile_,
        'user': user,
    }
    return render(request, 'user/profile.html', context=context)


@login_required
def change_profile(request):
    user = request.user
    profile_ = Profile.objects.filter(user=user).first()

    if request.method == 'POST':
        u_form = CustomUserChangeForm(request.POST, instance=user)
        p_form = ProfileForm(request.POST, request.FILES, instance=profile_)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p = p_form.save(commit=False)
            p.user = user
            p.save()
            return redirect('profile')
    u_form = CustomUserChangeForm(instance=user)
    p_form = ProfileForm(instance=profile_)
    context = {'u_form': u_form,
               'p_form': p_form,
               'profile': profile_
               }

    return render(request, 'user/profile_change.html', context=context)


@login_required
def book_list(request):
    books = Book.objects.filter(user=request.user)
    query = request.GET.get('q')
    is_read_filter = request.GET.get('is_read')
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    if is_read_filter in ['true', 'false']:
        books = books.filter(is_read=(is_read_filter == 'true'))
    return render(request, 'books/book_list.html', {'books': books})


@login_required
def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        book = form.save(commit=False)
        book.user = request.user
        book.save()
        return redirect('book_list')
    return render(request, 'books/book_form.html', {'form': form})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/book_form.html', {'form': form})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

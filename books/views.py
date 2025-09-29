from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Book
from .forms import CustomUserCreationForm, CustomAuthenticationForm, BookForm
import ssl
from django.conf import settings
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser 


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ignore SSL cert verification (testing only)
            ssl._create_default_https_context = ssl._create_unverified_context
            send_mail(
                'Welcome!',
                'Thanks for registering.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

            login(request, user)
            return redirect('book_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'books/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            ssl._create_default_https_context = ssl._create_unverified_context
            send_mail(
                'Login Alert',
                f'Hi {user.email}, you have successfully logged in.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            return redirect('book_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'books/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def book_list(request):
    books = Book.objects.filter(user=request.user) 
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)  
    return render(request, 'books/book_detail.html', {'book': book})


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  
    return render(request, 'books/book_confirm_delete.html', {'book': book})






# ===== Request Password Reset =====
def request_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = CustomUser.objects.filter(email=email).first()  

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"

            send_mail(
                "Password Reset Request",
                f"Click the link below to reset your password:\n\n{reset_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            messages.success(request, f"Password reset link sent to {email}.")
            return redirect("login")
        else:
            messages.error(request, "Email not found. Please check your email.")

    return render(request, "books/request_password_reset.html")


# ===== Reset Password =====
def reset_password(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = CustomUser.objects.filter(pk=uid).first()

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("password")
            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                return render(request, "books/reset_password.html")

            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful! You can now login.")
            return redirect("login")

        return render(request, "books/reset_password.html")
    else:
        messages.error(request, "Invalid or expired link.")
        return redirect("request_password_reset")



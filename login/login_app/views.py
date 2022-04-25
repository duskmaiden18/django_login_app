from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'login_app/index.html')

def sign_up(request):

    if request.method == "GET":
        form = UserCreationForm()
        return render(request, 'login_app/sign_up.html', context={'form': form})

    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('login_app/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'login_app/sign_up_success.html')
        else:
            form = UserCreationForm(request.POST)
            return render(request, 'login_app/sign_up.html', context={'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login_app:logged')
    else:
        return render(request, 'login_app/invalid_token.html')

def sign_in(request):

    if request.method == "GET":
        form = AuthenticationForm()
        return render(request, 'login_app/sign_in.html', context={'form': form})

    elif request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('login_app:logged')
                else:
                    return render(request, 'login_app/not_active_acc.html')
            else:
                form = AuthenticationForm(request, data=request.POST)
                return render(request, 'login_app/sign_in.html', context={'form': form})
        else:
            form = AuthenticationForm(request, data=request.POST)
            return render(request, 'login_app/sign_in.html', context={'form': form})

@login_required
def log_out(request):
    logout(request)
    return redirect('login_app:index')

@login_required
def logged(request):
    user = request.user
    return render(request, 'login_app/logged.html', context={"user": user})




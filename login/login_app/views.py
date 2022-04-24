from django.shortcuts import render
from .forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import login

from django.http import HttpResponse


# Create your views here.

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
                'token': PasswordResetTokenGenerator(),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'login_app/sign_up_success.html')
        else:
            form = UserCreationForm(request.POST)
            form.add_error('email', 'not valid')
            return render(request, 'login_app/sign_up.html', context={'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and PasswordResetTokenGenerator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token

# Sign Up View
class SignUpView(View):
    template_name = 'html_pages/signup.htm'
    def get(self,request,*args, **kwargs):
        form = SignUpForm(request.POST)
        return render(request,self.template_name,{'form':form})

    def post(self,request,*args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active= False #deactive account till is not confirmed
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('html_pages/acc_active_email.htm', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('/')
        return render(request, self.template_name, {'form': form})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_staff = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('/')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/')


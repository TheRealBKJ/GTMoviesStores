from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
import uuid
from .models import PasswordResetToken
from django.contrib.auth import update_session_auth_hash


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] ='The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})


def password_reset(request):
    template_data = {'title': 'Reset Password'}

    if request.method == 'GET':
        return render(request, 'accounts/password_reset.html', {'template_data': template_data})

    elif request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
            reset_token.token = str(uuid.uuid4())
            reset_token.save()
            template_data['message'] = f'Your reset token: {reset_token.token}'
        except User.DoesNotExist:
            template_data['error'] = 'User not found'

        return render(request, 'accounts/password_reset.html', {'template_data': template_data})




def password_reset_confirm(request):
    template_data = {'title': 'Confirm Reset Password'}

    if request.method == 'GET':
        return render(request, 'accounts/password_reset_confirm.html', {'template_data': template_data})

    elif request.method == 'POST':
        username = request.POST.get('username')
        token = request.POST.get('token')
        new_password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            reset_token = PasswordResetToken.objects.get(user=user, token=token)

            # Update the user's password
            user.set_password(new_password)
            user.save()

            # Keep the user logged in after resetting the password
            update_session_auth_hash(request, user)

            # Delete the token after successful reset
            reset_token.delete()

            return redirect('accounts.password_reset_success')  # Redirect to a success page

        except (User.DoesNotExist, PasswordResetToken.DoesNotExist):
            template_data['error'] = 'Invalid token or username'

        return render(request, 'accounts/password_reset_confirm.html', {'template_data': template_data})

def password_reset_success(request):
    return render(request, 'accounts/password_reset_success.html')
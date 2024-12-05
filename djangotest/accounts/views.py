from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm



# Create your views here.
def signup(request):
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Adjust this to the correct URL name for your home page.
    else:
        form = AuthenticationForm()

    # Render the correct template with the form.
    return render(request, 'accounts/login.html', {'form': form})
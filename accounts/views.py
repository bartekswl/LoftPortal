from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required





def login(request):

    if request.method == 'POST':
        email = request.POST['login_email']
        password = request.POST['login_password']

        user = auth.authenticate(email=email, password=password)
        

        if user == None:
            print("Wrong crednetials")

        else:
            if user.is_staff == True:
                auth.login(request, user)
                print("Success!")
                return redirect('dashboard')
            else:
                print('peasant')
                auth.login(request, user)
                return redirect('show_all')


    return render(request, 'accounts/login.html')



@login_required(login_url = 'login')
def logout(request):

    auth.logout(request)
  
    return redirect('login')

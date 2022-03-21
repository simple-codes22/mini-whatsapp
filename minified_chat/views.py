from django.shortcuts import redirect, render
from .models import Group, Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def index(request, *args, **kwargs):
    groups = Group.objects.all()
    return render(request, 'mini_index.html', {'groups': groups})

def login_register(request, process, *args, **kwargs):
    if process not in ('login', 'register', 'chat', 'admin'):
        return redirect('HomePage')
    if request.method == 'POST':
        if process == 'register':
            try:
                user_ = User.objects.create_user(
                    username=request.POST['username'],
                    first_name=request.POST['first-name'],
                    last_name=request.POST['last-name'],
                    email=request.POST['e-mail'],
                    password=request.POST['password']
                )
                # Simeon come back to this place as soon as possible
                user_stance = authenticate(
                    request, 
                    username=request.POST['username'], 
                    password=request.POST['password']
                )

                if user_stance is not None:
                    login(request, user_stance)
                    return redirect('HomePage')
                
            except Exception:
                print('Something went wrong during registration')
        
        elif process == 'login':
            try: 
                user_stance = authenticate(
                request,
                username=request.POST['username'], 
                password=request.POST['password']
            )

                if user_stance is not None:
                    login(request, user_stance)
            
            except Exception:
                print('Something went wrong in the login system')
        return render(request, 'login_register.html', {"process": process})

@login_required(login_url='/login/')
def group_page(request, group_name, *args, **kwargs):
    group_ = Group.objects.get(group_name=group_name)
    message_ = Message.objects.filter(group=group_).order_by('date_time_sent')
    return render(request, 'mini_group.html', {
        "group_object_details": group_,
        "messages": message_,
    })

@login_required(login_url='/login/')
def logout_page(request, *args, **kwargs):
    logout(request)
    return redirect('HomePage')

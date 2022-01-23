from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    #Instantiate 2 forms, pass in the user instance, to have the username and email filled in u_form, image filled in p_form
    if request.method == 'POST': #When we submit our form and possibly update the data
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                    request.FILES,      #images uploaded
                                    instance=request.user.profile)
        #Update the forms
        if u_form.is_valid() and p_form.is_valid():     
            u_form.save()
            p_form.save()
        #Get feedback to user and redirect them to profile page
        messages.success(request, f'Your account has been updated!')
        return redirect('profile')          
        #redirect instead of fall down to render function, because of the Post-get redirect pattern, if reload after submitted a form, there will be a message
        #warning there will be a resubmission --> run another post request, but redirect will send a get request instead of post
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    #pass in for template
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
from django.contrib.auth.decorators import login_required
from a_core.forms import UserProfileForm
from a_core.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def home_view(request):
    return render(request, 'a_core/home.html', {})


def profile_view(request):

    context = {
        'user': request.user,
        'profile': request.user.userprofile if hasattr(request.user, 'userprofile') else None
    }

    return render(request, 'a_core/profile.html', context)

@login_required
def update_profile(request):
    
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            
            form.save()
            
            return redirect('home') 
        
    else:
        
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'a_core/user_profile.html', context)
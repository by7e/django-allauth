from django.contrib.auth.decorators import login_required
from a_core.forms import UserProfileForm, CatAdoptionForm
from a_core.models import UserProfile, Cats, AdoptionRequest, CatPicture
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required

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

@login_required
def add_cat(request):
    if request.method == 'POST':
        form = CatAdoptionForm(request.POST)

        files = request.FILES.getlist('cat_images')

        if form.is_valid():
            cat = form.save(commit=False)
            cat.publisher = request.user
            cat.save()
            
            for f in files:
                CatPicture.objects.create(cat=cat, image=f)
            return redirect('list_cats')
    else:
        form = CatAdoptionForm()
    
    context = {
        'form': form
    }
    return render(request, 'a_core/add_cat.html', context)

def ListCats(request):
    cats = Cats.objects.filter(is_adopted=False)

    context = {
        "cats": cats,
        "user": request.user
    }

    return render(request, 'a_core/cats.html', context)

def cat_detail(request, cat_id):
    cat = get_object_or_404(Cats, id=cat_id)
    pictures = CatPicture.objects.filter(cat=cat)

    context = {
        "cat": cat,
        "pictures": pictures
    }

    return render(request, 'a_core/cat_details.html', context)
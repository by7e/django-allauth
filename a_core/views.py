from django.contrib.auth.decorators import login_required
from a_core.forms import UserProfileForm, CatAdoptionForm
from a_core.models import UserProfile, Cats, AdoptionRequest, CatPicture
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.db import transaction

# Create your views here.
def home_view(request):
    return render(request, 'a_core/home.html', {})

@login_required
def profile_view(request):

    context = {
        'user': request.user,
        'profile': request.user.userprofile if hasattr(request.user, 'userprofile') else None
    }

    return render(request, 'a_core/profile.html', context)

@login_required
def other_profile_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    cats = Cats.objects.filter(publisher=user_profile.user, is_adopted=False)

    context = {
        'profile': user_profile,
        'cats': cats
    }

    return render(request, 'a_core/other_profile.html', context)

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

@login_required
def ListCats(request):
    cats = Cats.objects.filter(is_adopted=False)

    context = {
        "cats": cats,
        "user": request.user
    }

    return render(request, 'a_core/cats.html', context)

@login_required
def cat_detail(request, cat_id):
    cat = get_object_or_404(Cats, id=cat_id)
    pictures = CatPicture.objects.filter(cat=cat)
    adoption_requests = None
    accepted_request = False

    if request.user == cat.publisher:
        adoption_requests = AdoptionRequest.objects.filter(
            cat=cat,
            status=AdoptionRequest.Status.PENDING
        ).select_related('requester')
    else:
        adoption_requests = AdoptionRequest.objects.filter(
            cat=cat,
            requester=request.user
        ).first()

        if adoption_requests and adoption_requests.status == AdoptionRequest.Status.APPROVED:
            accepted_request = True
    
    context = {
        "cat": cat,
        "pictures": pictures,
        "adoption_requests": adoption_requests,
        "accepted_request": accepted_request
    }

    return render(request, 'a_core/cat_details.html', context)

def request_adoption(request, cat_id):
    cat = get_object_or_404(Cats, id=cat_id)
    if request.user != cat.publisher:
        existing_request = AdoptionRequest.objects.filter(cat=cat, requester=request.user).first()
        if existing_request is None:
            AdoptionRequest.objects.create(cat=cat, requester=request.user)
    return redirect('cat_details', cat_id=cat.id)


@login_required
def accept_adoption_request(request, adoption_request_id):
    adoption_request = get_object_or_404(AdoptionRequest, id=adoption_request_id)
    if request.user != adoption_request.cat.publisher:
        return HttpResponseForbidden("You need to be the owner of this cat to accept adoption requests")
    
    if adoption_request.cat.is_adopted:
        return HttpResponse("This cat has already been adopted")

    with transaction.atomic():
        adoption_request.status = AdoptionRequest.Status.APPROVED
        cat = adoption_request.cat
        cat.is_adopted = True
        cat.adopter = adoption_request.requester
        cat.save()
        adoption_request.save()

    
    AdoptionRequest.objects.filter(
        cat=cat,
        status=AdoptionRequest.Status.PENDING
    ).exclude(id=adoption_request.id).update(status=AdoptionRequest.Status.REJECTED)
        

    return redirect('cat_details', cat_id=adoption_request.cat.id)

# cancel adoption request view can be added here in future
@login_required
def cancel_adoption_request(request, adoption_request_id):
    adoption_request = get_object_or_404(AdoptionRequest, id=adoption_request_id)
    if request.user != adoption_request.requester:
        return HttpResponseForbidden("You can only cancel your own adoption requests")
    
    if adoption_request.status != AdoptionRequest.Status.PENDING:
        return HttpResponse("You can only cancel pending adoption requests")

    adoption_request.delete()
    return redirect('cat_details', cat_id=adoption_request.cat.id)
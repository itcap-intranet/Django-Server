from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user_profile.crud.user_profile_crud import get_user_profile

# Create your views here.
@login_required
def profile(request):

    context = {
        'user_profile': get_user_profile(request),
    }

    return render(request, "profile/profile.html", context)


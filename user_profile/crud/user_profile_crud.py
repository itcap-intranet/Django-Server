from user_profile.models import UserProfile
from django.shortcuts import redirect, render
from user_profile.forms import UserProfileForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('user_profile.view_userprofile', raise_exception=True)
def get_user_profile(request):
    user = request.user
    user_profile, create = UserProfile.objects.get_or_create(user=user, first_name=user.first_name, last_name=user.last_name)
    return user_profile


@login_required
@permission_required('user_profile.change_userprofile', raise_exception=True)
def profile_update(request):
    user_profile = get_user_profile(request)

    print('update profile')
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
    print(form)

    if form.is_valid():
        user_profile = form.save()
        return HttpResponseRedirect('/profile/view/')
    else:
        print('form is not valid')
        print(form.errors)
        error = form.errors

    context = {
        'user_profile': user_profile,
    }

    return render(request, "profile/profile.html", context)

from courses.models import LessonVideo, LessonChapter
from courses.forms import VideoForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required


# @login_required
# @permission_required('courses.add_lessonvideo', raise_exception=True)
def video_create_view(request):
    print('create video view')
    if request.method == 'POST':
        form = VideoForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            print(form.cleaned_data)
            video = form.save()
            form = VideoForm()
        else:
            print('form is not valid')
            print(form.errors)
    else:
        form = VideoForm()

    data = {
        'form': form,
        'videos': get_videos(request),
    }

    return render(request, "settings/sections/upload_video_settings.html", data)

# @login_required
# @permission_required('courses.view_lessonvideo', raise_exception=True)
def get_videos(request):
    videos = LessonVideo.objects.all()
    return videos


# @login_required
# @permission_required('courses.change_lessonvideo', raise_exception=True)
def video_edit_view(request, video_id):
    video = get_object_or_404(LessonVideo, id=video_id)
    video_chapters = LessonChapter.objects.filter(type='Video')

    print('edit lesson chapter view')
    form = VideoForm(request.POST or None, instance=video)

    if form.is_valid():
        video = form.save()
        return HttpResponseRedirect('/settings/videos', {'form': form})
    else:
        print('form is not valid')
        print(form.errors)
        error = form.errors

    context = {
        'video': video,
        'video_chapters': video_chapters,
    }
    return render(request, "settings/sections/forms/edit_video.html", context)


# @login_required
# @permission_required('courses.delete_lessonvideo', raise_exception=True)
def video_delete_view(request, video_id):
    video = get_object_or_404(LessonVideo, id=video_id)
    video.delete()
    return HttpResponseRedirect('/settings/videos')

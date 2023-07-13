from courses.models import Author
from courses.forms import AuthorForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required


def get_global_context(request):
    return {
        'authors': get_authors(request),
    }


# @login_required
# @permission_required('courses.add_author', raise_exception=True)
def author_create_view(request):
    print('create author view')
    if request.method == 'POST':
        form = AuthorForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            print(form.cleaned_data)
            author = form.save()
            form = AuthorForm()
        else:
            print('form is not valid')
            print(form.errors)
    else:
        form = AuthorForm()

    data = {
        'form': form,
        'authors': get_authors(request),
    }

    return render(request, "settings/sections/author_settings.html", data)


# @login_required
# @permission_required('courses.view_author', raise_exception=True)
def get_authors(request):
    authors = Author.objects.all()
    return authors


# @login_required
# @permission_required('courses.change_author', raise_exception=True)
def author_edit_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    print('edit author view')
    form = AuthorForm(request.POST or None, request.FILES or None, instance=author)

    if form.is_valid():
        author = form.save()
        return HttpResponseRedirect('/settings/authors', {'form': form})
    else:
        print('form is not valid')
        print(form.errors)
        error = form.errors

    context = {
        'author': author,
    }
    return render(request, "settings/sections/forms/edit_author.html", context)


# @login_required
# @permission_required('courses.delete_author', raise_exception=True)
def author_delete_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return HttpResponseRedirect('/settings/authors')

from django.urls import path, include
from . import views as progress_views
from .crud.user_assignment_crud import submit_assignment_view, ThanksForAssignmentView, user_assignment_delete_view
from .crud.user_quiz_crud import submit_quiz_view, user_quiz_delete_view
from .views import get_my_progress, leaderboard
from django.contrib.auth.decorators import login_required

app_name = 'progress'

urlpatterns = [
    path('submit_quiz/<int:quiz_id>', submit_quiz_view, name='submit-quiz'),
    path('submit_assignment/', submit_assignment_view, name='submit-assignment'),
    # path('thanks_for_assignment/', login_required(ThanksForAssignmentView.as_view()), name='thanks-for-assignment'),
    path('delete_user_assignment/<int:user_assignment_id>', user_assignment_delete_view, name='user-assignment-delete'),

    path('delete_user_quiz/<int:user_quiz_id>', user_quiz_delete_view, name='user-quiz-delete'),

    path('my_progress/', get_my_progress, name='my-progress'),
    path('leaderboard/', leaderboard, name='leaderboard'),

]
from django import forms
from .models import UserAssignmentSubmission, UserQuizSubmission
from courses.models import QuizQuestion


class AssignmentSubmissionForm(forms.ModelForm):

    class Meta:
        model = UserAssignmentSubmission
        fields = ['assignment_id', 'submission_file']

class QuizSubmissionForm(forms.Form):

    quiz_id = forms.IntegerField()
    form_data = {}


    def __init__(self, *args, **kwargs):
        self.quiz_id = kwargs.pop('quiz_id', None)
        super(QuizSubmissionForm, self).__init__(*args, **kwargs)
        data = self.data
        # print(self.data)
        quiz_id1 = data.get('quiz_id')

        questions = QuizQuestion.objects.filter(quiz_id=quiz_id1)

        for question in questions:
            field_name = 'radios-'+str(question.id)
            field_value = data.get(field_name)
            # print("saving " + field_name + " with value " + field_value)
            self.form_data[field_name] = field_value

        # print("form data")
        # print(self.form_data)

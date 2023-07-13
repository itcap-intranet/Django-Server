from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name","last_name", "email")



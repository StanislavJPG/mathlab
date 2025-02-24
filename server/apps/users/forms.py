from allauth.account.forms import SignupForm


class UserLoginForm(SignupForm):
    # is_own = forms.BooleanField()

    def save(self, request):
        user = super().save(request)

        # Add your own processing here.

        # You must return the original result.
        return user

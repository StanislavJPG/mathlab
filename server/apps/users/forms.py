from allauth.socialaccount.forms import SignupForm as SocialSignupForm


class CustomSignupForm(SocialSignupForm):
    ...
    # def save(self, request):
    #
    #     # Ensure you call the parent class's save.
    #     # .save() returns a User object.
    #     user = super().save(request)
    #     raise Exception('HERE')
    #     # Add your own processing here.
    #
    #     # You must return the original result.
    #     return user

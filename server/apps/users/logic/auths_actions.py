from allauth.account.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'allauth_templates/login.html'

    # def form_valid(self, form):
    #     form_valid = super().form_valid(form)

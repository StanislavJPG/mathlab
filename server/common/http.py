from django.shortcuts import redirect


def base_redirect(request):
    return redirect("mathlab:base-math-news")

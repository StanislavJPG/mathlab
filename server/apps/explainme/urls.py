from django.urls import path

from server.apps.explainme.logic.searcher import explain_me

urlpatterns = [path("explainme/", explain_me, name="explainme")]

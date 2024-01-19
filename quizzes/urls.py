from django.urls import path
from .views.quiz import api_quizzes, api_quiz_view, add_quiz
from .views.flashcard import flashcard_view, all_flashcards_view, add_flashcard_view

urlpatterns = [
    path("api/quizzes/all", api_quizzes, name="api_quizzes"),
    path("api/quizzes/quiz/<uuid:id>", api_quiz_view, name="api quiz view"),
    path("api/quizzes/add", add_quiz, name="add quiz"),
    path("flashcard/<uuid:id>/<str:title>", flashcard_view, name="flashcard_view"),
    path("flashcards/all", all_flashcards_view, name="all flashcards"),
    path("flashcards/add", add_flashcard_view, name="add flashcard")
]
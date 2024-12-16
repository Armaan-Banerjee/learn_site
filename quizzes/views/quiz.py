from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from ..models import Flashcard, Keyword, Quiz, QuizQuestion, QuizAnswer
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def api_quizzes(request):
    quizzes = Quiz.objects.all()
    
    quizlist = [quiz.full_quiz_two() for quiz in quizzes]
    
    outdict = {"quizzes": quizlist}

    return JsonResponse(outdict)

def api_quiz_view(request, id):
    
    quiz = get_object_or_404(Quiz, id=id)

    quizdict = quiz.full_quiz_two()

    return JsonResponse(quizdict)

def quiz_view(request, id):
    quiz = get_object_or_404(Quiz, id=id)

    questions = quiz.all_questions()
    template = loader.get_template("quizview.html")

    context = {
        "quiz": quiz,
        "questions": questions
    }

    return HttpResponse(template.render(context, request))


@csrf_exempt
def add_quiz(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            quiz = Quiz.add_quiz_from_dict(data)
        except TypeError:
            return HttpResponse("Dict must contain a list for questions and answers" ,status=400)

        return HttpResponseRedirect(f"/api/quizzes/quiz/{quiz.id}")
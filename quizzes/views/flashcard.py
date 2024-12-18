from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from ..models import Flashcard, Keyword, Quiz, QuizQuestion, QuizAnswer
from django.views.decorators.csrf import csrf_exempt
from info.services.slugs import slugify
from quizzes.forms import CreateFlashCardTags
from users.models import User
# Create your views here.

@csrf_exempt
def add_flashcard_view(request):

    if request.method == "POST":
        post = request.POST
        items = post.items()
        title = ""
        userid = ""
        cards = []
        private = True
        tags = []

        for key, value in items:
            if key == "title":
                title = value
            elif key == "userid":
                userid = value 
            elif key == "csrfmiddlewaretoken":
                continue
            elif key == "private":
                if value != "private":
                    private = False
            elif key == "tags":
                form = CreateFlashCardTags(request.POST)
                if form.is_valid():
                    selected_tags = form.cleaned_data['tags']  
                    tags = selected_tags
            else:
                cards.append(post.getlist(key))
        
        new_flashcard = Flashcard.add_flashcard(title=slugify(title), userid=userid, private=private)

        for tag in tags:
            new_flashcard.add_tag(tag)

        for card in cards:
            front = card[0]
            back = card[1]
            new_keyword = Keyword.add_keyword(front=front, back=back, flashcard=new_flashcard)
        
        return HttpResponseRedirect(f"/flashcard/{new_flashcard.id}/{new_flashcard.title}")

        #val_cards = [post.getlist(val) for val in cards]
        
    form = CreateFlashCardTags()

    context = {
        "form": form,
    }        

    template = loader.get_template("addflashcard.html")
    
    return HttpResponse(template.render(context=context, request=request))


def flashcard_view(request, id, title):
    flashcard = get_object_or_404(Flashcard, id=id)

    tags = flashcard.all_tags()
    
    if flashcard.private:
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponse("No can do")
        if current_user.id != flashcard.user.id:
            return HttpResponse("you are not allowed ")
    
    template = loader.get_template("flashcard.html")
    
    context = {
        "flashcard": flashcard,
        "keywords": flashcard.all_cards(),
        "User_x": flashcard.user, 
        "tags": tags,
    }

    return HttpResponse(template.render(context, request))

def all_flashcards_view(request):
    flashcards = Flashcard.all_public()

    user_flashcards = []
    if request.user.is_authenticated:
        user = request.user
        user_flashcards = user.get_flashcards()

    template = loader.get_template("allflashcards.html")

    context = {
        "flashcards": flashcards,
        "usercards": user_flashcards
    }

    return HttpResponse(template.render(context, request))

def delete_flashcard_view(request):
    userid = request.GET.get("userid")
    cardid = request.GET.get("cardid")
    user_x = get_object_or_404(User, id=userid)

    card = get_object_or_404(Flashcard, id=cardid)
    if card.user == user_x:
        card.delete_flashcard()
        return HttpResponseRedirect("/flashcards/all")
    else:
        return HttpResponse(status=403)



from django.db import models
import uuid
from users.models import User
from info.services.slugs import slugify

# Create your models here.

class Flashcard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    private = models.BooleanField(default=True)
    user = models.ForeignKey("users.User", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} | {self.title}"

    @staticmethod
    def all_public():
        return Flashcard.objects.filter(private=False)
    
    def all_cards(self):
        return self.keyword_set.all()
    
    @staticmethod
    def add_flashcard(title, userid, private=True):
        user = User.objects.get(id=userid)
        new = Flashcard(title=title, user=user, private=private)
        new.save()

        return new

class Keyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    front = models.TextField()
    back  = models.TextField()
    flashcard = models.ForeignKey("Flashcard", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} | {self.front}"
    
    @staticmethod
    def add_keyword(front, back, flashcard):

        new_keyword = Keyword(front=front, back=back, flashcard=flashcard)
        new_keyword.save()

        return new_keyword

class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = ("Quizzes")

    def __str__(self):
        return f"{self.id} | {self.title}"

    @staticmethod
    def add_quiz_from_dict(data : dict):
        
        title = data["title"] 
        quiz = Quiz(title=slugify(title))  

        quiz.save()

        questions = data["questions"]
        if type(questions) != list:
            raise TypeError("Must be a list")

        for question in questions:
            ques = question["question"]
            q = QuizQuestion.add_question(ques, quiz)

            answers = question["answers"]
            
            if type(answers) != list:
                raise TypeError("Must be a list")

            for answer in answers:
                QuizAnswer.add_answer(answer, q)

        return quiz


    def all_questions(self):
        return self.quizquestion_set.all()
    
    def full_quiz(self):
        outdict = {}
        questions = self.all_questions()
        for question in questions:
            answers = question.all_answers()
            
            answerdict = {}
            for ans in answers:
                answerdict[str(ans.id)] = ans.answer
            
            outdict[str(question.id)] = [question.question, answerdict]
        
        return outdict
    
    def full_quiz_two(self):
        outdict = {}

        outdict["title"] = self.title
        outdict["id"] = self.id

        outdict["questions"] = []

        questions = self.all_questions()
        for question in questions:
            answers = question.all_answers_names_id()

            ques_dict = {}
            ques_dict["question"] = question.question
            ques_dict["id"] = question.id

            ques_dict["answers"] = answers

            outdict["questions"].append(ques_dict)
        
        return outdict


class QuizQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    quiz = models.ForeignKey("Quiz", blank=True, null=True, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = ("Questions")

    def __str__(self):
        return f"{self.id} | {self.question}"

    @staticmethod
    def add_question(question, quiz):
        
        question = QuizQuestion(question=question, quiz=quiz)
        question.save()

        return question

    def all_answers(self):
        return self.quizanswer_set.all()

    def all_answers_names(self):
        answers = self.quizanswer_set.all()
        out = [ans.answer for ans in answers]
        return out

    def all_answers_names_id(self):
        answers = self.quizanswer_set.all()
        out = [(ans.answer, ans.id) for ans in answers]
        return out    


class QuizAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer = models.TextField()
    question = models.ForeignKey("QuizQuestion", blank=True, null=True, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = ("Answers")

    def __str__(self):
        return f"{self.id} | {self.question}"

    @staticmethod
    def add_answer(answer : str, question: QuizQuestion):
        answer = QuizAnswer(answer=answer, question=question)

        answer.save()

        return answer
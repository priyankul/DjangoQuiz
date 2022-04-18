from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.views.generic import ListView

from questions.models import Question, Answer
from quizez.models import Quiz
from results.models import Result


def home(request):
    return render(request, 'quizez/home.html')


def signupUser(request):
    if request.method == 'GET':
        return render(request, 'quizez/signupUser.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/main')
            except IntegrityError:
                return render(request, 'quizez/signupUser.html', {'form': UserCreationForm(), 'error': 'Username has '
                                                                                                       'already '
                                                                                                       'exists. '
                                                                                                       'Please select '
                                                                                                       'new username'})
        else:
            return render(request, 'quizez/signupUser.html', {'form': UserCreationForm(), 'error': 'Passwords did not '
                                                                                                   'match'})


def loginUser(request):
    if request.method == 'GET':
        return render(request, 'quizez/loginUser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'quizez/loginUser.html', {'form': AuthenticationForm(), 'error': 'Username and '
                                                                                                    'password did not '
                                                                                                    'match'})
        else:
            login(request, user)
            return redirect('/main')


@login_required
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


class QuizListView(ListView):
    Model = Quiz
    template_name = 'quizez/main.html'
    context_object_name = "quiz"

    def get_queryset(self):
        return Quiz.objects.all()


@login_required
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizez/quiz.html', {'obj': quiz})


@login_required
def quiz_data_view(request, pk):

    quiz = Quiz.objects.get(pk=pk)
    question = []

    for q in quiz.get_questions():
        answer = []
        for a in q.get_answers():
            answer.append(a.text)
        question.append({str(q): answer})
    return JsonResponse({
        'data': question,
    })


@login_required
def save_quiz_view(request, pk):
    print(request.POST)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print("keys ", k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                print(a_selected)
                questions_answers = Answer.objects.filter(question=q)

                for a in questions_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append(
                    {str(q): {'correct_answer': correct_answer, 'answered': a_selected}})

            else:
                results.append({str(q): 'not answered'})
        final_res = score * multiplier
        print(final_res)
        Result.objects.create(quiz=quiz, user=user, score=final_res)
        if final_res > 40:
            return JsonResponse({'passed': True, 'score': final_res, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': final_res, 'results': results})


@login_required
def results(request):
    results = Result.objects.all()
    return render(request, "quizez/results.html", {'results': results})

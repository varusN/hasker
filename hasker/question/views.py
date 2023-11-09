from django.http import HttpResponse, HttpRequest
from django.utils import timezone
from django.views.generic import TemplateView,ListView, CreateView
from django.shortcuts import render, get_object_or_404

from .models import Question
from .models import Answer
from .forms import QuestionForm

# class QuestionList(ListView):
#     model = Question
#     fields = "subject", "description"

class Questions(ListView):
    """ List of questions sorted by posted time.
    """

    model = Question
    paginate_by = 20
    ordering = ("-created_date", "-pk")
    context_object_name = 'questions'
    template_name = "question/question_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("author")


# def question_list(request):
#     questions = Question.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
#     return render(request, 'question/question_list.html', {'questions': questions})

def answers(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question/details.html', {'question': question})

def ask_question(request):
    form = QuestionForm()
    return render(request, 'question/ask_question.html', {'form': form})
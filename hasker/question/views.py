from django.http import HttpResponse, HttpRequest
from django.utils import timezone
from django.views.generic import TemplateView,ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Q


from .models import Question
from .models import Answer
from .forms import QuestionForm

class Trends:
    extra_context = {
        "trands": Question.trending(count=10),
    }
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["trending"] = Question.trending(count=10)
    #     return context

class Questions(Trends, ListView):
    template_name = "question/question_list.html"
    model = Question
    paginate_by = 20
    context_object_name = 'questions'
    queryset = (
        Question
        .objects
        .order_by("?")
        .all()
    )
class LatestQuestions(Questions):
    ordering = ("-created_date")

class TopQuestions(Questions):
    ordering = ("-votes", "-created_date")


class SearchQuestions(Questions):
    ordering = ("-votes", "-created_date")
    query = ""

    def get(self, *args, **kwargs):
        self.query = self.request.GET.get("q", "").strip()

        if not self.query:
            raise Http404("Query should be specified.")

        if "tag:" in self.query:
            *_, tag = self.query.partition(":")
            tag = tag.strip().lower()
            if tag:
                return redirect("tag", tag=tag)
        return super().get(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(Q(subject__icontains=self.query) | Q(description__icontains=self.query))
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["query"] = self.query
        return context


class TagQuestions(Questions):
    ordering = ("-votes", "-created_date")

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.kwargs["tag"].strip().lower()
        qs = qs.filter(tags__name=tag)
        return qs


def answers(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question/details.html', {'question': question})

def ask_question(request):
    form = QuestionForm()
    return render(request, 'question/ask_question.html', {'form': form})
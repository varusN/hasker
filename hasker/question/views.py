import time
from django.http import HttpResponse, HttpRequest
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Q, F
from django.urls import reverse_lazy
from django.db import transaction

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
                return redirect("question:tag", tag=tag)
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
        qs = qs.filter(tag__name=tag)
        return qs


def details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'question/details.html', {'question': question})

class Details(Trends, View):
    template_name = "question/question_list.html"

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=self.pk)
        return render(request,
                      self.template_name,
                      {'question': question},
                      )
def post():
    print('AAAAAAAAAA')
def vote_up(self):
    print('UP')
    reporter = Question.objects.get(pk=self.pk)
    reporter.stories_filed = F('votes') + 1
    reporter.save()

def vote_down(self):
    reporter = Question.objects.get(pk=self.pk)
    reporter.stories_filed = F('votes') - 1
    reporter.save()


class AskQuestion(Trends, LoginRequiredMixin, CreateView):

    form_class = QuestionForm
    model = Question
    template_name = "question/ask_question.html"
    success_url = reverse_lazy("question:latest")

    @transaction.atomic
    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()

        raw_tags = form.cleaned_data["tags"]
        question.add_tags(raw_tags, self.request.user)

        messages.success(
            self.request, "Your question posted!"
        )
        return redirect(self.success_url)
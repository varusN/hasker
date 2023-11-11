import time
from django.http import HttpResponse, HttpRequest
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView,ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Q, F
from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic.edit import UpdateView

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

class Trends():
    extra_context = {
        "trend": Question.trending(count=10)
    }


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
    ordering = ("-votes")

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
    form = QuestionForm(question_id, request.POST)
    if request.method == 'POST':
        if (request.POST['vote']):
            form = QuestionForm(question_id, request.POST)
            if (request.POST['vote'] == 'up'):
                question.votes += 1
            else:
                question.votes -= 1
            question.save()
            messages.success(request, "Thank you for voting!")
            return redirect('question:details', question_id=question_id)
    else:
        return render(request, 'question/details.html', {'question': question})

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


class EditQuestion(Trends, LoginRequiredMixin, UpdateView):
    model = Question
    pk_url_kwarg = "question_id"
    template_name = "question/update_question.html"
    fields = ["subject", "description"]
    def get_success_url(self) -> str:
        return reverse_lazy('question:details', kwargs={'question_id': self.object.pk})


class AnswerQuestion(Trends, LoginRequiredMixin, CreateView):
    form_class = AnswerForm
    model = Answer
    template_name = "question/answer.html"

    def get_success_url(self) -> str:
        return reverse_lazy('question:details', kwargs={'question_id': self.object.pk})

    @transaction.atomic
    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()

        messages.success(
            self.request, "Your answer posted!"
        )
        return redirect(self.success_url)
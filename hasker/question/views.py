import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView

from .forms import AnswerForm, QuestionForm
from .models import Answer, Question


class Trends:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["trend"] = Question.trending(count=10)
        return context


class Questions(Trends, ListView):
    template_name = "question/question_list.html"
    model = Question
    paginate_by = 20
    context_object_name = "questions"
    queryset = Question.objects.order_by("?").all()


class LatestQuestions(Questions):
    ordering = "-created_date"


class TopQuestions(Questions):
    ordering = "-votes"


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
        qs = qs.filter(
            Q(subject__icontains=self.query) | Q(description__icontains=self.query)
        )
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

    try:
        answers = Answer.objects.filter(question=question_id)
    except Answer.DoesNotExist:
        answers = None
    if request.method == "POST":
        if request.POST["vote"]:
            req = request.POST["vote"].split(",")
            if req[0] == "up":
                question.votes += 1
                question.save()
            elif req[0] == "down":
                question.votes -= 1
                question.save()
            elif req[0] == "answer_up":
                answer = get_object_or_404(Answer, pk=req[1])
                answer.votes += 1
                answer.save()
            elif req[0] == "answer_down":
                answer = get_object_or_404(Answer, pk=req[1])
                answer.votes -= 1
                answer.save()
            elif req[0] == "correct":
                answer = get_object_or_404(Answer, pk=req[1])
                answer.is_correct += 1
                answer.save()
            messages.success(request, "Thank you for voting!")
            return redirect("question:details", question_id=question_id)
    else:
        return render(
            request, "question/details.html", {"question": question, "answers": answers}
        )


class AskQuestion(Trends, LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    model = Question
    template_name = "question/ask_question.html"
    success_url = reverse_lazy("question:latest")

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()

        tags = form.cleaned_data["tags"]
        question.add_tags(tags)
        messages.success(self.request, "Your question posted!")
        return HttpResponseRedirect(
            reverse("question:details", kwargs={"question_id": question.id})
        )


class EditQuestion(Trends, LoginRequiredMixin, UpdateView):
    model = Question
    pk_url_kwarg = "question_id"
    template_name = "question/update_question.html"
    fields = ["subject", "description"]

    def form_valid(self, form):
        question = form.save(commit=False)
        messages.success(self.request, "Your answer changed!")
        return HttpResponseRedirect(
            reverse(
                "question:details", kwargs={"question_id": self.kwargs["question_id"]}
            )
        )


class AnswerQuestion(Trends, LoginRequiredMixin, CreateView):
    form_class = AnswerForm
    model = Answer
    pk_url_kwarg = "question_id"
    context_object_name = "answers"
    question = None
    template_name = "question/answer.html"

    def get_initial(self):
        return {"question": self._get_question().id}

    def _get_question(self):
        if self.question is None:
            pk = self.kwargs.get("question_id", None)
            self.question = Question.get_question(pk)
        return self.question

    def get_context_data(self, **kwargs):
        context = super(AnswerQuestion, self).get_context_data(**kwargs)
        context["question"] = self._get_question()
        return context

    def answered(self, *args):
        question_id = self.kwargs["question_id"]
        question = get_object_or_404(Question, pk=question_id)
        question.answers += 1
        question.save()

    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.author = self.request.user
        self.answered(self)
        answer.save()
        messages.success(self.request, "Your answer posted!")
        return HttpResponseRedirect(
            reverse(
                "question:details", kwargs={"question_id": self.kwargs["question_id"]}
            )
        )

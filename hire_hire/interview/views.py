from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic import ListView, TemplateView
from django.conf import settings

from .exceptions import CustomException
from .models import (
    Duel,
    DuelPlayer,
    DuelQuestion,
    Interview,
    Language,
    Question
)


class Languages(ListView):
    model = Language
    template_name = 'pages/interviews.html'


class Index(TemplateView):
    template_name = 'pages/index.html'


class InterviewSettings(TemplateView):
    template_name = 'pages/test-settings.html'

    def post(self, request, *args, **kwargs):
        count = request.POST.get(
            'questions-count', default=settings.DEFAULT_QUESTIONS_COUNT
        )

        try:
            count = int(count)
        except CustomException:
            count = settings.DEFAULT_QUESTIONS_COUNT

        questions = Question.objects.random(count)
        options = dict()
        if request.user.is_authenticated:
            options['user'] = request.user

        interview = Interview.objects.create(**options)
        interview.questions.add(*questions)

        return HttpResponseRedirect(
            reverse(
                'interview:interview',
                kwargs={'interview_id': interview.pk}
            )
        )


class InterviewFlow(TemplateView):
    template_name = 'pages/challenge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interview = get_object_or_404(Interview, pk=kwargs.get('interview_id'))
        context['questions'] = interview.questions.all()
        return context


class InterviewFinish(TemplateView):
    template_name = 'pages/test-finished.html'


class DuelSettings(TemplateView):
    template_name = 'pages/duel-settings.html'

    def post(self, request, *args, **kwargs):
        options = request.POST
        count = options.get(
            'duel-questions-count', default=settings.DEFAULT_QUESTIONS_COUNT
        )

        try:
            count = int(count)
        except CustomException:
            count = settings.DEFAULT_QUESTIONS_COUNT

        questions = Question.objects.random(count)
        user = None
        if request.user.is_authenticated:
            user = request.user
        duel = Duel.objects.create(owner=user)
        DuelPlayer.objects.create(name=options.get('player1'), duel=duel)
        DuelPlayer.objects.create(name=options.get('player2'), duel=duel)
        duel_questions = (
            DuelQuestion(
                duel=duel,
                is_answered=False,
                question=question
            ) for question in questions
        )
        DuelQuestion.objects.bulk_create(duel_questions)

        return HttpResponseRedirect(
            reverse(
                'interview:duel',
                kwargs={'duel_id': duel.pk}
            )
        )


class DuelFlowQuestion(TemplateView):

    template_name = 'pages/duel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        duel = get_object_or_404(
            Duel.objects.select_related(),
            pk=kwargs.get('duel_id')
        )
        context['duel_id'] = duel.pk
        duel_question = duel.questions.filter(is_answered=False).first()
        if duel_question:
            context['duel_question'] = duel_question
        context['player1'] = duel.players.first()
        context['player2'] = duel.players.last()
        context['can_choose_winner'] = False
        return context

    def _finish_duel(self, context):
        if context.get('duel_question') is None:
            return HttpResponseRedirect(
                reverse(
                    'interview:duel_finish',
                    kwargs={'duel_id': context.get('duel_id')}
                )
            )
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self._finish_duel(context)


class DuelFlowAnswered(DuelFlowQuestion):

    template_name = 'pages/duel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_choose_winner'] = True
        duel_question = context.get('duel_question')
        if duel_question:
            duel_question.is_answered = True
            duel_question.save()
        return context

    def post(self, request, *args, **kwargs):
        duel = get_object_or_404(
            Duel.objects.select_related(),
            pk=kwargs.get('duel_id')
        )
        winner_id = int(request.POST.get('duel-radio-player'))
        if duel.players.filter(pk=winner_id).exists():
            winner = duel.players.filter(pk=winner_id).first()
            winner.counter += 1
            winner.save()
        else:
            duel.wrong_answers += 1
            duel.save()
        return HttpResponseRedirect(
            reverse(
                'interview:duel',
                kwargs={'duel_id': duel.pk}
            )
        )


class DuelFinish(TemplateView):

    template_name = 'pages/duel-results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        duel = get_object_or_404(
            Duel.objects.select_related(),
            pk=kwargs.get('duel_id')
        )
        context['duel'] = duel
        context['player1'] = duel.players.first()
        context['player2'] = duel.players.last()
        return context
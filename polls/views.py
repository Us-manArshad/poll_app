from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Questions, Choice
from django.shortcuts import get_object_or_404, render 
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Questions.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Questions
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Questions.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Questions
    template_name = 'polls/results.html'


# def index(request):
#     latest_question_list = Questions.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Questions, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Questions, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'questions': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

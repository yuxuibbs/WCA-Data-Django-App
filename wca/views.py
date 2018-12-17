from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse
from django.urls import reverse_lazy
from django_filters.views import FilterView

from .models import Person
from .models import Result
from .models import Competition

from wca.forms import PersonForm
from wca.forms import ResultForm

from .filters import ResultFilter
from .filters import PersonFilter

class HomePageView(generic.TemplateView):
    template_name = 'wca/home.html'


class CompetitionListView(generic.ListView):
    model = Competition
    context_object_name = 'competitions'
    template_name = 'wca/competitions.html'
    paginate_by = 200

    def get_queryset(self):
        return Competition.objects.all().order_by('competition_name')

class CompetitionDetailView(generic.DetailView):
    model = Competition
    context_object_name = 'competition'
    template_name = 'wca/competition_detail.html'


class ResultFilterView(FilterView):
    filterset_class = ResultFilter
    template_name = 'wca/result_filter.html'


class ResultDetailView(generic.DetailView):
    model = Result
    context_object_name = 'result'
    template_name = 'wca/result_detail.html'

@method_decorator(login_required, name='dispatch')
class ResultCreateView(generic.View):
    model = Result
    form_class = ResultForm
    success_message = "Result created successfully"
    template_name = 'wca/result_new.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        form = ResultForm(request.POST)
        if form.is_valid():
            result_info = form.save(commit=False)
            result_info.save()
            for competition in form.cleaned_data['competition']:
                Result.objects.create(result=result_info, competition=competition)
            return HttpResponseRedirect(result_info.get_absolute_url())
        return render(request, 'wca/result_new.html', {'form': form})

    def get(self, request):
        form = ResultForm()
        return render(request, 'wca/result_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ResultUpdateView(generic.UpdateView):
    model = Result
    form_class = ResultForm
    context_object_name = 'result'
    success_message = "Result updated successfully"
    template_name = 'wca/result_update.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        result_info = form.save(commit=False)
        result_info.save()

        old_ids = Result.objects\
            .values_list('result_id', flat=True)\
            .filter(result_id=result_info.result_id)

        new_competitions = form.cleaned_data['competition']
        new_events = form.cleaned_data['event']

        new_ids = []

        for competition in new_competitions:
            new_id = competition.competition_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                Result.objects \
                    .create(result=result_info, competition=competition)

        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                Result.objects \
                    .filter(result_id=result_info.result_id, competition_id=old_id) \
                    .delete()

        return HttpResponseRedirect(result_info.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class ResultDeleteView(generic.DeleteView):
    model = Result
    success_message = "Result deleted successfully"
    success_url = reverse_lazy('people')
    context_object_name = 'result'
    template_name = 'wca/result_delete.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        Result.objects \
            .filter(result_id=self.object.result_id) \
            .delete()

        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

class PersonListView(generic.ListView):
    model = Person
    context_object_name = 'people'
    template_name = 'wca/people.html'
    paginate_by = 4000

    def get_queryset(self):
        return Person.objects.all().order_by('person_name')

class PersonFilterView(FilterView):
    filterset_class = PersonFilter
    template_name = 'wca/person_filter.html'


class PersonDetailView(generic.DetailView):
    model = Person
    context_object_name = 'person'
    template_name = 'wca/person_detail.html'


@method_decorator(login_required, name='dispatch')
class PersonCreateView(generic.View):
    model = Person
    form_class = PersonForm
    success_message = "Person created successfully"
    template_name = 'wca/person_new.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def post(self, request):
        personForm = PersonForm(request.POST)
        resultForm = ResultForm(request.POST)
        print(personForm.is_valid())
        print(resultForm.is_valid())
        if personForm.is_valid() and resultForm.is_valid():
            person_info = personForm.save(commit=False)
            person_info.save()
            result_info = resultForm.save(commit=False)
            result_info.save()
            print(person_info)
            print(result_info)
            # Result.objects.create(person=person_info, competition=competition)
            return HttpResponseRedirect(person_info.get_absolute_url())
        return render(request, 'wca/person_new.html', {'personForm': personForm, 'resultForm': resultForm})

    def get(self, request):
        personForm = PersonForm()
        resultForm = ResultForm()
        return render(request, 'wca/person_new.html', {'personForm': personForm, 'resultForm': resultForm})

@method_decorator(login_required, name='dispatch')
class PersonUpdateView(generic.UpdateView):
    model = Person
    form_class = PersonForm
    context_object_name = 'person'
    success_message = "Person updated successfully"
    template_name = 'wca/person_update.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        person_info = form.save(commit=False)
        person_info.save()

        old_ids = Result.objects\
            .values_list('person_id', flat=True)\
            .filter(person_id=person_info.person_id)

        new_competitions = form.cleaned_data['competition']

        new_ids = []

        for competition in new_competitions:
            new_id = competition.competition_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                Result.objects \
                    .create(person=person_info, competition=competition)

        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                Result.objects \
                    .filter(person_id=person_info.person_id, competition_id=old_id) \
                    .delete()

        return HttpResponseRedirect(person_info.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class PersonDeleteView(generic.DeleteView):
    model = Person
    success_message = "Person deleted successfully"
    success_url = reverse_lazy('people')
    context_object_name = 'person'
    template_name = 'wca/person_delete.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        Result.objects \
            .filter(person_id=self.object.person_id) \
            .delete()

        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())



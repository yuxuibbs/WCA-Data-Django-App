import django_filters
from wca.models import Result, Person, Competition, Event, EventFormat, RoundType, Country


class ResultFilter(django_filters.FilterSet):
    competition = django_filters.ModelChoiceFilter(
        field_name='competition',
        label='Competition Name',
        queryset=Competition.objects.all().order_by('competition_name'),
        lookup_expr='exact'
    )

    event = django_filters.ModelChoiceFilter(
        field_name='event',
        label='Event',
        queryset=Event.objects.all().order_by('event_name'),
        lookup_expr='exact'
    )

    event_format = django_filters.ModelChoiceFilter(
        field_name='event_format',
        label='Event Format',
        queryset=EventFormat.objects.all().order_by('event_format_name'),
        lookup_expr='exact'
    )

    round_type = django_filters.ModelChoiceFilter(
        field_name='round_type',
        label='Round Type',
        queryset=RoundType.objects.all().order_by('round_type_name'),
        lookup_expr='exact'
    )

    person_name = django_filters.CharFilter(
        field_name='person_name',
        label='Competitior Name',
        lookup_expr='icontains'
    )

    person = django_filters.ModelChoiceFilter(
        field_name='person',
        label='WCA ID',
        queryset=Person.objects.all().order_by('person_identifier'),
        lookup_expr='exact'
    )

    class Meta:
        model = Result
        fields = []


class PersonFilter(django_filters.FilterSet):
    person_name = django_filters.CharFilter(
        field_name='person_name',
        label='Competitior Name',
        lookup_expr='icontains'
    )

    person_identifier = django_filters.ModelChoiceFilter(
        field_name='person_identifier',
        label='WCA ID',
        queryset=Person.objects.all().order_by('person_identifier'),
        lookup_expr='exact'
    )

    country = django_filters.ModelChoiceFilter(
        field_name='country',
        label='Country',
        queryset=Country.objects.all().order_by('country_name'),
        lookup_expr='exact'
    )

    gender = django_filters.ModelChoiceFilter(
        field_name='gender',
        label='Gender',
        queryset=Person.objects.all().order_by('gender'),
        lookup_expr='exact'
    )

    class Meta:
        model = Person
        fields = []
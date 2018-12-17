from wca.models import Continent, Event, EventFormat, RoundType, Country, Competition, Person, Result, RankAverage, RankSingle
from rest_framework import response, serializers, status


class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = ('continent_id', 'continent_identifier', 'continent_name', 'record_name', 'latitude', 'longitude')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('event_id', 'event_identifier', 'event_name', 'rank')


class EventFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFormat
        fields = ('event_format_id', 'event_format_identifier', 'event_format_name', 'sort_by', 'sort_by_second', 'expected_solve_count', 'trim_fastest_n', 'trim_slowest_n')


class RoundTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundType
        fields = ('round_type_id', 'round_type_identifier', 'rank', 'round_type_name', 'final')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('country_id', 'country_identifier', 'country_name', 'continent_id')


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('competition_id', 'competition_identifier', 'competition_name', 'city_name', 'country_id', 'information', 'year', 'month', 'day', 'end_month', 'end_day', 'event_specs', 'wca_delegate', 'organiser', 'venue', 'venue_address', 'venue_details', 'external_website', 'latitude', 'longitude')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('person_id', 'person_identifier', 'person_name', 'country_id', 'gender')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('result_id', 'competition_id', 'event_id', 'round_type_id', 'pos', 'best', 'average', 'person_name', 'person_id', 'event_format_id', 'value1', 'value2', 'value3', 'value4', 'value5', 'regional_single_record', 'regional_average_record')


class RankAverageSerializer(serializers.ModelSerializer):
    person_id = PersonSerializer(many=False, read_only=True)
    event_id = EventSerializer(many=False, read_only=True)

    class Meta:
        model = RankAverage
        fields = ('rank_average_id', 'person_id', 'event_id', 'best', 'world_rank', 'continent_rank', 'country_rank')


class RankSingleSerializer(serializers.ModelSerializer):
    person_id = PersonSerializer(many=False, read_only=True)
    event_id = EventSerializer(many=False, read_only=True)

    class Meta:
        model = RankSingle
        fields = ('rank_single_id', 'person_id', 'event_id', 'best', 'world_rank', 'continent_rank', 'country_rank')


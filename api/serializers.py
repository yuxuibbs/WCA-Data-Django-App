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


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('result_id', 'competition_id', 'event_id', 'round_type_id', 'pos', 'best', 'average', 'person_name', 'person_id', 'event_format_id', 'value1', 'value2', 'value3', 'value4', 'value5', 'regional_single_record', 'regional_average_record')

class PersonSerializer(serializers.ModelSerializer):
    person_identifier = serializers.CharField(
        allow_blank=False,
        max_length=10
    )
    person_name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        max_length=80
    )
    country = CountrySerializer(
        many=False,
        read_only=True
    )
    country_id = serializers.PrimaryKeyRelatedField(
        allow_null=False,
        many=False,
        write_only=True,
        queryset=Country.objects.all(),
        source='country'
    )
    gender = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        max_length=1
    )
    result = ResultSerializer(
        source='result_set',
        many=True,
        read_only=True
    )
    result_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Result.objects.all(),
        source='result'
    )

    class Meta:
        model = Person
        fields = ('person_id', 'person_identifier', 'person_name', 'country', 'country_id', 'gender', 'result', 'result_ids')

    def create(self, validated_data):
        results = validated_data.pop('result')
        person = Person.objects.create(**validated_data)

        if results is not None:
            for result in results:
                Result.objects.create(competition_id=result.competition_id, event_id=result.event_id, round_type_id=result.round_type_id, pos=result.pos, best=result.best, average=result.average, person_name=result.person_name, person_id=person.person_id, event_format_id=result.event_format_id, value1=result.value1, value2=result.value2, value3=result.value3, value4=result.value4, value5=result.value5)

        return person


    def update(self, instance, validated_data):
        instance.person_identifier = validated_data.get('person_identifier', instance.person_identifier)
        instance.person_name = validated_data.get('person_name', instance.person_name)
        instance.country_id = validated_data.get('country_id', instance.country_id)
        instance.gender = validated_data.get('gender', instance.gender)

        old_country_id = Person.objects.filter(person_id=instance.person_id)[0].country_id
        new_country_name = validated_data.pop('country')
        new_country_id = Country.objects.filter(country_name=new_country_name)[0].country_id
        if old_country_id != new_country_id:
            instance.country_id = new_country_id

        instance.save()
        return instance


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


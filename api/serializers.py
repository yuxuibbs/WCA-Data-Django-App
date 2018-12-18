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
    competition = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Result.objects.all(),
        source='result'
    )

    class Meta:
        model = Person
        fields = ('person_id', 'person_identifier', 'person_name', 'country_id', 'gender')

    def create(self, validated_data):
        person = Person.objects.create(**validated_data)
        return person

    def update(self, instance, validated_data):
        instance.person_identifier = validated_data.get('person_identifier', instance.person_identifier)
        instance.person_name = validated_data.get('person_name', instance.person_name)
        instance.country_id = validated_data.get('country_id', instance.country_id)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance



class ResultSerializer(serializers.ModelSerializer):
    competition_id = CompetitionSerializer(many=False)
    event_id = EventSerializer(many=False)
    round_type_id = RoundTypeSerializer(many=False)
    pos = serializers.IntegerField()
    best = serializers.IntegerField()
    average = serializers.IntegerField()
    person_name = serializers.CharField(max_length=80, allow_blank=True, allow_null=True)
    person_id = PersonSerializer(many=True)
    event_format_id = EventFormatSerializer(many=False)
    value1 = serializers.IntegerField()
    value2 = serializers.IntegerField()
    value3 = serializers.IntegerField()
    value4 = serializers.IntegerField()
    value5 = serializers.IntegerField()

    class Meta:
        model = Result
        fields = ('result_id', 'competition_id', 'event_id', 'round_type_id', 'pos', 'best', 'average', 'person_name', 'person_id', 'event_format_id', 'value1', 'value2', 'value3', 'value4', 'value5', 'regional_single_record', 'regional_average_record')

    def create(self, validated_data):
        print(validated_data)
        result = Result.objects.create(**validated_data)
        return result

    def update(self, instance, validated_data):
        competition_id = validated_data.get('competition_id', instance.competition_id)
        event_id = validated_data.get('event_id', instance.event_id)
        round_type_id = validated_data.get('round_type_id', instance.round_type_id)
        pos = validated_data.get('pos', instance.pos)
        best = validated_data.get('best', instance.best)
        average = validated_data.get('average', instance.average)
        person_name = validated_data.get('person_name', instance.person_name)
        person_id = validated_data.get('person_id', instance.person_id)
        event_format_id = validated_data.get('event_format_id', instance.event_format_id)
        value1 = validated_data.get('value1', instance.value1)
        value2 = validated_data.get('value2', instance.value2)
        value3 = validated_data.get('value3', instance.value3)
        value4 = validated_data.get('value4', instance.value4)
        value5 = validated_data.get('value5', instance.value5)
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


from django.db import models
from django.urls import reverse
from django.db.models import F


class Continent(models.Model):
    continent_id = models.IntegerField(primary_key=True)
    continent_identifier = models.CharField(max_length=50)
    continent_name = models.CharField(max_length=50)
    record_name = models.CharField(max_length=3)
    latitude = models.IntegerField()
    longitude = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'continent'
        ordering = ['continent_name']
        verbose_name = 'Continent'
        verbose_name_plural = 'Continents'

    def __str__(self):
        return self.continent_name


class Event(models.Model):
    event_id = models.IntegerField(primary_key=True)
    event_identifier = models.CharField(max_length=6)
    event_name = models.CharField(max_length=54)
    rank = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'event'
        ordering = ['event_name']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.event_name


class EventFormat(models.Model):
    event_format_id = models.IntegerField(primary_key=True)
    event_format_identifier = models.CharField(max_length=1)
    event_format_name = models.CharField(max_length=50)
    sort_by = models.CharField(max_length=255)
    sort_by_second = models.CharField(max_length=255)
    expected_solve_count = models.IntegerField()
    trim_fastest_n = models.IntegerField()
    trim_slowest_n = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'event_format'
        ordering = ['event_format_name']
        verbose_name = 'Event Format'
        verbose_name_plural = 'Event Formats'

    def __str__(self):
        return self.event_format_name


class RoundType(models.Model):
    round_type_id = models.IntegerField(primary_key=True)
    round_type_identifier = models.CharField(max_length=1)
    rank = models.IntegerField()
    round_type_name = models.CharField(max_length=50)
    final = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'round_type'
        ordering = ['round_type_name']
        verbose_name = 'Round Type'
        verbose_name_plural = 'Round Types'

    def __str__(self):
        return self.round_type_name


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_identifier = models.CharField(max_length=50)
    country_name = models.CharField(max_length=50)
    continent = models.ForeignKey(Continent, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'country'
        ordering = ['country_name']
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.country_name


class Competition(models.Model):
    competition_id = models.AutoField(primary_key=True)
    competition_identifier = models.CharField(max_length=32)
    competition_name = models.CharField(max_length=50)
    city_name = models.CharField(max_length=50)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    information = models.TextField(blank=True, null=True)
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    day = models.PositiveSmallIntegerField()
    end_month = models.PositiveSmallIntegerField()
    end_day = models.PositiveSmallIntegerField()
    event_specs = models.CharField(max_length=256, blank=True, null=True)
    wca_delegate = models.TextField(blank=True, null=True)
    organiser = models.TextField(blank=True, null=True)
    venue = models.CharField(max_length=240)
    venue_address = models.CharField(max_length=120, blank=True, null=True)
    venue_details = models.CharField(max_length=120, blank=True, null=True)
    external_website = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.IntegerField(blank=True, null=True)
    longitude = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competition'
        ordering = ['competition_name']
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'

    def __str__(self):
        return self.competition_name


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    person_identifier = models.CharField(max_length=10)
    person_name = models.CharField(max_length=80, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    gender = models.CharField(max_length=1, blank=True, null=True)

    competition = models.ManyToManyField(Competition, through='Result')

    class Meta:
        managed = False
        db_table = 'person'
        ordering = ['person_identifier']
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        return "{} - {}".format(self.person_name, self.person_identifier)

    def person_display(self):
        return "{} - {}".format(self.person_name, self.person_identifier)

    def get_absolute_url(self):
        return reverse('person_detail', kwargs={'pk': self.pk})

    @property
    def competition_list(self):
        competitions = self.competition.select_related().values(name=F('competition_name')).distinct().order_by('year', 'month', 'day')
        competition_names = []
        for competition in competitions:
            competition_names.append(competition['name'])
        return str(len(competition_names)) + ' - ' + ', '.join(competition_names)


class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    round_type = models.ForeignKey('RoundType', on_delete=models.PROTECT)
    pos = models.SmallIntegerField()
    best = models.IntegerField()
    average = models.IntegerField()
    person_name = models.CharField(max_length=80, blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event_format = models.ForeignKey(EventFormat, on_delete=models.PROTECT)
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    value3 = models.IntegerField()
    value4 = models.IntegerField()
    value5 = models.IntegerField()
    regional_single_record = models.CharField(max_length=3, blank=True, null=True)
    regional_average_record = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'result'
        ordering = ['competition', 'person_name', 'event', 'pos', 'average']
        verbose_name = 'Result'
        verbose_name_plural = 'Results'

    def __str__(self):
        return "Event: {} | Position: {} | Name: {} | Attempt 1: {} | Attempt 2: {} | Attempt 3: {} | Attempt 4: {} | Attempt 5: {} | Average: {}| Best: {}".format(self.event, self.pos, self.person_name, self.value1, self.value2, self.value3, self.value4, self.value5, self.average, self.best)
    
    def get_absolute_url(self):
        return reverse('result_detail', kwargs={'pk': self.pk})


class RankAverage(models.Model):
    rank_average_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    best = models.IntegerField()
    world_rank = models.IntegerField()
    continent_rank = models.IntegerField()
    country_rank = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rank_average'
        ordering = ['world_rank']
        verbose_name = 'Rank for Average'
        verbose_name_plural = 'Ranks for Average'

    def __str__(self):
        return "World Rank: {} | Continent Rank: {} | National Rank: {}".format(self.world_rank, self.continent_rank, self.country_rank)


class RankSingle(models.Model):
    rank_single_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    best = models.IntegerField()
    world_rank = models.IntegerField()
    continent_rank = models.IntegerField()
    country_rank = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rank_single'
        ordering = ['world_rank']
        verbose_name = 'Rank for Single'
        verbose_name_plural = 'Ranks for Single'

    def __str__(self):
        return "World Rank: {} | Continent Rank: {} | National Rank: {}".format(self.world_rank, self.continent_rank, self.country_rank)


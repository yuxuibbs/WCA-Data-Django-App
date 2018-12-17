from django.contrib import admin

import wca.models as models

@admin.register(models.Continent)
class ContinentAdmin(admin.ModelAdmin):
    fields = ['continent_name', 'record_name', 'latitude', 'longitude']
    list_display = ['continent_name', 'record_name', 'latitude', 'longitude']
    ordering = ['continent_name']

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    fields = ['event_name', 'rank']
    list_display = ['event_name', 'rank']
    ordering = ['event_name']

@admin.register(models.EventFormat)
class EventFormatAdmin(admin.ModelAdmin):
    fields = ['event_format_name']
    list_display = ['event_format_name']
    ordering = ['event_format_name']

@admin.register(models.RoundType)
class RoundTypeAdmin(admin.ModelAdmin):
    fields = ['round_type_name']
    list_display = ['round_type_name']
    ordering = ['round_type_name']

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    fields = ['country_name', 'continent']
    list_display = ['country_name', 'continent']
    ordering = ['country_name']

@admin.register(models.Competition)
class Admin(admin.ModelAdmin):
    fields = ['competition_name', 'city_name', 'country', 'information', 'year', 'month', 'day', 'end_month', 'end_day', 'event_specs', 'wca_delegate', 'organiser', 'venue', 'venue_address', 'venue_details', 'latitude', 'longitude']
    list_display = ['competition_name', 'city_name', 'country', 'information', 'year', 'month', 'day', 'end_month', 'end_day', 'event_specs', 'wca_delegate', 'organiser', 'venue', 'venue_address', 'venue_details', 'latitude', 'longitude']
    ordering = ['competition_name']

@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ['person_name', 'person_identifier', 'country', 'gender']
    list_display = ['person_name', 'person_identifier', 'country', 'gender']
    ordering = ['person_name', 'person_identifier']

@admin.register(models.Result)
class ResultAdmin(admin.ModelAdmin):
    fields = ['competition', 'event', 'round_type', 'pos', 'best', 'average', 'person_name', 'person', 'event_format', 'value1', 'value2', 'value3', 'value4', 'value5', 'regional_single_record', 'regional_average_record']
    list_display = ['competition', 'event', 'round_type', 'pos', 'best', 'average', 'person_name', 'person', 'event_format', 'value1', 'value2', 'value3', 'value4', 'value5', 'regional_single_record', 'regional_average_record']
    ordering = ['competition', 'event', 'round_type', 'pos', 'best', 'average', 'person_name']

@admin.register(models.RankAverage)
class RankAverageAdmin(admin.ModelAdmin):
    fields = ['person', 'event', 'best', 'world_rank', 'continent_rank', 'country_rank']
    list_display = ['person', 'event', 'best', 'world_rank', 'continent_rank', 'country_rank']
    ordering = ['event', 'world_rank']

@admin.register(models.RankSingle)
class RankSingleAdmin(admin.ModelAdmin):
    fields = ['person', 'event', 'best', 'world_rank', 'continent_rank', 'country_rank']
    list_display = ['person', 'event', 'best', 'world_rank', 'continent_rank', 'country_rank']
    ordering = ['event', 'world_rank']

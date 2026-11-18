from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse

from .models import (
    Sport, League, Season, Club, Team,
    Match, Athlete, KPICategory, KPI, PlayerMatchKPI
)

# Register your models here.

@admin.action(description="Edit selected item")
def edit_selected_item(modeladmin, request, queryset):
    if queryset.count() != 1:
        modeladmin.message_user(
            request,
            "Please select exactly one item to edit.",
            level=messages.WARNING,
        )
        return
    obj = queryset.first()
    url = reverse(
        f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
        args=[obj.pk],
    )
    return redirect(url)


# Register the Edit action globally so it appears in the Action menu on every screen
admin.site.add_action(edit_selected_item)


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('sport_id', 'name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('league_id', 'name', 'abbreviation')
    search_fields = ('name', 'abbreviation')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('season_id', 'season_name', 'league', 'start_date', 'end_date', 'is_active')
    list_filter = ('league', 'is_active')
    search_fields = ('season_name',)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('club_id', 'name', 'sport', 'phone', 'url')
    list_filter = ('sport',)
    search_fields = ('name', 'address')


class AthleteInline(admin.TabularInline):
    model = Athlete
    extra = 1
    fields = ('jersey_number', 'first_name', 'last_name', 'position', 'is_active')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'name', 'club')
    list_filter = ('club',)
    search_fields = ('name',)
    inlines = [AthleteInline]


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('athlete_id', 'jersey_number', 'first_name', 'last_name', 'team', 'position', 'is_active')
    list_filter = ('team', 'position', 'is_active')
    search_fields = ('first_name', 'last_name')


class PlayerMatchKPIInline(admin.TabularInline):
    model = PlayerMatchKPI
    extra = 1
    autocomplete_fields = ('player', 'kpi')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'season', 'home_team', 'away_team', 'home_score', 'away_score', 'match_datetime', 'court_location')
    list_filter = ('season', 'home_team', 'away_team')
    search_fields = ('court_location', 'home_team__name', 'away_team__name')
    inlines = [PlayerMatchKPIInline]


@admin.register(KPICategory)
class KPICategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'description')
    search_fields = ('category_name',)


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ('kpi_id', 'kpi_name', 'category', 'target_value')
    list_filter = ('category',)
    search_fields = ('kpi_name', 'description')


@admin.register(PlayerMatchKPI)
class PlayerMatchKPIAdmin(admin.ModelAdmin):
    list_display = ('performance_id', 'match', 'player', 'kpi', 'actual_value', 'target_value', 'recorded_at')
    list_filter = ('kpi__category', 'kpi', 'match__season')
    search_fields = ('player__first_name', 'player__last_name', 'kpi__kpi_name')
    autocomplete_fields = ('player', 'kpi')

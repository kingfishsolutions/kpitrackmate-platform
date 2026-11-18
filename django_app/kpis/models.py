from django.db import models

class Sport(models.Model):
    sport_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sport'

    def __str__(self):
        return self.name


class League(models.Model):
    league_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=15)

    class Meta:
        db_table = 'league'

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        db_column='league_id',
        related_name='seasons'
    )
    season_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'season'

    def __str__(self):
        return f"{self.league.abbreviation} - {self.season_name}"


class Club(models.Model):
    club_id = models.AutoField(primary_key=True)
    sport = models.ForeignKey(
        Sport,
        on_delete=models.SET_NULL,
        db_column='sport_id',
        related_name='clubs',
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    class Meta:
        db_table = 'club'

    def __str__(self):
        return self.name


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    club = models.ForeignKey(
        Club,
        on_delete=models.SET_NULL,
        db_column='club_id',
        related_name='teams',
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'team'

    def __str__(self):
        return self.name


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        db_column='season_id',
        related_name='matches'
    )
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        db_column='home_team_id',
        related_name='home_matches'
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        db_column='away_team_id',
        related_name='away_matches'
    )
    match_datetime = models.TimeField()
    court_location = models.CharField(max_length=100, blank=True, null=True)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)

    class Meta:
        db_table = 'match'
        verbose_name_plural = 'matches'

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.match_datetime})"


class Athlete(models.Model):
    athlete_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        db_column='team_id',
        related_name='athletes',
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    jersey_number = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'athlete'

    def __str__(self):
        number = f"#{self.jersey_number} " if self.jersey_number is not None else ""
        return f"{number}{self.first_name} {self.last_name}"


class KPICategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'kpi_category'
        verbose_name = 'KPI Category'
        verbose_name_plural = 'KPI Categories'

    def __str__(self):
        return self.category_name


class KPI(models.Model):
    kpi_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        KPICategory,
        on_delete=models.CASCADE,
        db_column='category_id',
        related_name='kpis'
    )
    kpi_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    target_value = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    class Meta:
        db_table = 'kpi'
        verbose_name = 'KPI'
        verbose_name_plural = 'KPIs'

    def __str__(self):
        return f"{self.kpi_name} ({self.category.category_name})"


class PlayerMatchKPI(models.Model):
    performance_id = models.AutoField(primary_key=True)
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        db_column='match_id',
        related_name='player_kpis'
    )
    player = models.ForeignKey(
        Athlete,
        on_delete=models.CASCADE,
        db_column='player_id',
        related_name='match_kpis'
    )
    kpi = models.ForeignKey(
        KPI,
        on_delete=models.CASCADE,
        db_column='kpi_id',
        related_name='player_performances'
    )
    actual_value = models.DecimalField(max_digits=10, decimal_places=2)
    target_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'player_match_kpis'
        verbose_name = 'Player Match KPI'
        verbose_name_plural = 'Player Match KPIs'

    def __str__(self):
        return f"{self.player} - {self.kpi.kpi_name}: {self.actual_value}"

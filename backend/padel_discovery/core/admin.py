from django.contrib import admin

from .models import Coach, Court, SearchLog, Tournament


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "hourly_price", "google_rating", "updated_at")
    list_filter = ("city",)
    search_fields = ("name", "city", "address")


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "experience_years", "verified")
    list_filter = ("city", "verified")
    search_fields = ("name", "city", "specialties")


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "date", "entry_fee")
    list_filter = ("city", "date")
    search_fields = ("title", "city", "venue")


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ("query", "response_time_ms", "created_at")
    search_fields = ("query",)

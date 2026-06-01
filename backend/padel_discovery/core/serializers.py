from __future__ import annotations

from rest_framework import serializers

from .models import Coach, Court, SearchLog, Tournament


class CourtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Court
        fields = "__all__"


class CoachSerializer(serializers.ModelSerializer):
    specialties_list = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = "__all__"

    def get_specialties_list(self, obj: Coach) -> list[str]:
        return [item.strip() for item in obj.specialties.split(",") if item.strip()]


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = "__all__"


class SearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchLog
        fields = "__all__"


class SearchFilterSerializer(serializers.Serializer):
    city = serializers.CharField(required=False, allow_blank=False, max_length=100)
    max_price = serializers.IntegerField(required=False, min_value=0)
    min_experience_years = serializers.IntegerField(required=False, min_value=0)
    verified = serializers.BooleanField(required=False)
    specialties = serializers.ListField(child=serializers.CharField(max_length=50), required=False, allow_empty=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    category = serializers.ChoiceField(choices=["courts", "coaches", "tournaments", "all"], required=False)
    text = serializers.CharField(required=False, allow_blank=True, max_length=255)

    def validate(self, attrs):
        if "date_from" in attrs and "date_to" in attrs and attrs["date_from"] > attrs["date_to"]:
            raise serializers.ValidationError("date_from cannot be after date_to.")
        return attrs


class SearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField(min_length=2, max_length=255)
    filters = SearchFilterSerializer(required=False)
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    page_size = serializers.IntegerField(required=False, min_value=1, max_value=24, default=8)


class SearchResponseSerializer(serializers.Serializer):
    query = serializers.CharField()
    filters = SearchFilterSerializer()
    results = serializers.ListField(child=serializers.DictField())
    count = serializers.IntegerField()
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()
    response_time_ms = serializers.IntegerField()
    search_log = SearchLogSerializer()

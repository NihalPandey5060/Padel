from __future__ import annotations

from time import perf_counter

from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Coach, Court, SearchLog, Tournament
from .serializers import (
    CoachSerializer,
    CourtSerializer,
    SearchFilterSerializer,
    SearchLogSerializer,
    SearchRequestSerializer,
    SearchResponseSerializer,
    TournamentSerializer,
)
from .services import gemini_filters


class CourtViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__iexact=city)
        return queryset


class CoachViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__iexact=city)
        return queryset


class TournamentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__iexact=city)
        return queryset


def _apply_court_filters(queryset, filters: dict):
    if city := filters.get("city"):
        queryset = queryset.filter(city__icontains=city)
    if max_price := filters.get("max_price"):
        queryset = queryset.filter(hourly_price__lte=max_price)
    if text := filters.get("text"):
        queryset = queryset.filter(Q(name__icontains=text) | Q(address__icontains=text) | Q(city__icontains=text) | Q(description__icontains=text))
    return queryset


def _apply_coach_filters(queryset, filters: dict):
    if city := filters.get("city"):
        queryset = queryset.filter(city__icontains=city)
    if min_experience := filters.get("min_experience_years"):
        queryset = queryset.filter(experience_years__gte=min_experience)
    if filters.get("verified") is True:
        queryset = queryset.filter(verified=True)
    if specialties := filters.get("specialties"):
        specialty_query = Q()
        for specialty in specialties:
            specialty_query |= Q(specialties__icontains=specialty)
        queryset = queryset.filter(specialty_query)
    if text := filters.get("text"):
        queryset = queryset.filter(Q(name__icontains=text) | Q(city__icontains=text) | Q(bio__icontains=text))
    return queryset


def _apply_tournament_filters(queryset, filters: dict):
    if city := filters.get("city"):
        queryset = queryset.filter(city__icontains=city)
    if date_from := filters.get("date_from"):
        queryset = queryset.filter(date__gte=date_from)
    if date_to := filters.get("date_to"):
        queryset = queryset.filter(date__lte=date_to)
    if text := filters.get("text"):
        queryset = queryset.filter(Q(title__icontains=text) | Q(city__icontains=text) | Q(venue__icontains=text) | Q(description__icontains=text))
    return queryset


@api_view(["POST"])
@permission_classes([AllowAny])
def search_view(request):
    started = perf_counter()
    serializer = SearchRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    query = serializer.validated_data["query"]
    page = serializer.validated_data["page"]
    page_size = serializer.validated_data["page_size"]
    explicit_filters = serializer.validated_data.get("filters", {})
    ai_filters = gemini_filters(query)
    combined = {**ai_filters, **explicit_filters}

    filter_serializer = SearchFilterSerializer(data=combined)
    filter_serializer.is_valid(raise_exception=True)
    filters = filter_serializer.validated_data

    category = filters.get("category", "all")
    combined_results = []

    if category in {"all", "courts"}:
        for court in _apply_court_filters(Court.objects.all(), filters):
            combined_results.append({"type": "court", **CourtSerializer(court).data})

    if category in {"all", "coaches"}:
        for coach in _apply_coach_filters(Coach.objects.all(), filters):
            combined_results.append({"type": "coach", **CoachSerializer(coach).data})

    if category in {"all", "tournaments"}:
        for tournament in _apply_tournament_filters(Tournament.objects.all(), filters):
            combined_results.append({"type": "tournament", **TournamentSerializer(tournament).data})

    combined_results.sort(key=lambda item: (item["type"], item.get("name") or item.get("title") or ""))
    count = len(combined_results)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    results = combined_results[start_index:end_index]

    response_time_ms = max(1, int((perf_counter() - started) * 1000))
    search_log = SearchLog.objects.create(query=query, response_time_ms=response_time_ms)

    response_payload = {
        "query": query,
        "filters": filters,
        "results": results,
        "count": count,
        "page": page,
        "page_size": page_size,
        "has_next": end_index < count,
        "has_previous": page > 1,
        "response_time_ms": response_time_ms,
        "search_log": SearchLogSerializer(search_log).data,
    }
    response_serializer = SearchResponseSerializer(response_payload)
    return Response(response_serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = authenticate(request, username=username, password=password)
    if user is None:
        raise ValidationError({"detail": "Invalid credentials."})

    refresh = RefreshToken.for_user(user)
    response = Response({"detail": "Login successful."}, status=status.HTTP_200_OK)
    response.set_cookie("access_token", str(refresh.access_token), httponly=True, secure=False, samesite="Lax", max_age=60 * 60 * 12)
    response.set_cookie("refresh_token", str(refresh), httponly=True, secure=False, samesite="Lax", max_age=60 * 60 * 24 * 7)
    return response


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_view(request):
    refresh_token = request.COOKIES.get("refresh_token") or request.data.get("refresh")
    if not refresh_token:
        raise ValidationError({"detail": "Refresh token is required."})

    serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
    serializer.is_valid(raise_exception=True)
    access_token = serializer.validated_data["access"]

    response = Response({"detail": "Token refreshed."}, status=status.HTTP_200_OK)
    response.set_cookie("access_token", access_token, httponly=True, secure=False, samesite="Lax", max_age=60 * 60 * 12)
    return response

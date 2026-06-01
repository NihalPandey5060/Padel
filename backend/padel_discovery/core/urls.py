from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CoachViewSet, CourtViewSet, TournamentViewSet, login_view, refresh_view, search_view

router = DefaultRouter()
router.register(r"courts", CourtViewSet, basename="court")
router.register(r"coaches", CoachViewSet, basename="coach")
router.register(r"tournaments", TournamentViewSet, basename="tournament")

urlpatterns = router.urls + [
    path("search/", search_view, name="search"),
    path("auth/login/", login_view, name="login"),
    path("auth/refresh/", refresh_view, name="refresh"),
]

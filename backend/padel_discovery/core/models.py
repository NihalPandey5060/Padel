from __future__ import annotations

from django.db import models


class Court(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    hourly_price = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    google_rating = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-google_rating", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"


class Coach(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, db_index=True)
    experience_years = models.PositiveSmallIntegerField()
    specialties = models.TextField(help_text="Comma-separated specialties")
    phone = models.CharField(max_length=20)
    bio = models.TextField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-verified", "-experience_years", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"


class Tournament(models.Model):
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=100, db_index=True)
    venue = models.CharField(max_length=200)
    date = models.DateField(db_index=True)
    entry_fee = models.PositiveIntegerField()
    description = models.TextField()
    registration_url = models.URLField()

    class Meta:
        ordering = ["date", "title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.city})"


class SearchLog(models.Model):
    query = models.CharField(max_length=255)
    response_time_ms = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.query

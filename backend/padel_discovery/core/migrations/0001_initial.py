from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Court",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(db_index=True, max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("hourly_price", models.PositiveIntegerField()),
                ("phone", models.CharField(max_length=20)),
                ("website", models.URLField(blank=True)),
                ("google_rating", models.DecimalField(decimal_places=1, max_digits=2)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Coach",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("city", models.CharField(db_index=True, max_length=100)),
                ("experience_years", models.PositiveSmallIntegerField()),
                ("specialties", models.TextField(help_text="Comma-separated specialties")),
                ("phone", models.CharField(max_length=20)),
                ("bio", models.TextField()),
                ("verified", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tournament",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("city", models.CharField(db_index=True, max_length=100)),
                ("venue", models.CharField(max_length=200)),
                ("date", models.DateField(db_index=True)),
                ("entry_fee", models.PositiveIntegerField()),
                ("description", models.TextField()),
                ("registration_url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="SearchLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("query", models.CharField(max_length=255)),
                ("response_time_ms", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

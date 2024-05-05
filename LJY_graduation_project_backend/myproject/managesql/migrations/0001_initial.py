# Generated by Django 5.0.3 on 2024-04-19 18:04

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TrainingInfo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("epoch", models.IntegerField()),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("duration", models.IntegerField(help_text="累计用时，单位秒")),
                ("user_id", models.IntegerField()),
                ("model", models.CharField(max_length=255)),
                ("top1_accuracy", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "top2_accuracy",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "top3_accuracy",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "top4_accuracy",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "top5_accuracy",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "top6_accuracy",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "top7_accuracy",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "top8_accuracy",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "top9_accuracy",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "top10_accuracy",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "optional_feature",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "learning_rate",
                    models.DecimalField(
                        blank=True, decimal_places=8, max_digits=10, null=True
                    ),
                ),
            ],
            options={
                "db_table": "training_info",
            },
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "users",
            },
        ),
    ]

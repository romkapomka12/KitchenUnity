# Generated by Django 4.2.5 on 2023-10-02 08:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0002_alter_cook_year_of_experience"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="unit",
            field=models.CharField(
                choices=[
                    ("g", "grams"),
                    ("ml", "milliliters"),
                    ("th", "Thing"),
                    ("te.sp.", "teaspoon"),
                    ("tb.sp.", "tablespoon"),
                    ("gl", "glass"),
                ],
                max_length=15,
            ),
        ),
    ]

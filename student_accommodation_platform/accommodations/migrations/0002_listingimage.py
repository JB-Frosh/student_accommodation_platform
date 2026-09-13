from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accommodations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ListingImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="listing-images/%Y/%m/")),
                ("caption", models.CharField(blank=True, max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="accommodations.listing",
                    ),
                ),
            ],
            options={"ordering": ["created_at"]},
        ),
    ]
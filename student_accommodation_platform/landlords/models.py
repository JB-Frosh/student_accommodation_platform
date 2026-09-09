from django.db import models


class Landlord(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, help_text="Contact phone number, e.g. 08012345678.")
    verified = models.BooleanField(default=False, help_text="Whether the landlord identity has been verified.")
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.name
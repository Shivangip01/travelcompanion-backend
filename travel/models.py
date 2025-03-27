from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()
    best_time_to_visit = models.CharField(max_length=100)
    rating = models.FloatField()

    # NEW FIELDS
    things_to_do = models.TextField(blank=True, null=True)
    local_food = models.TextField(blank=True, null=True)
    must_visit_places = models.TextField(blank=True, null=True)
    recommended_hotels = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

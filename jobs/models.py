from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    posted_date = models.DateField()
    details_url = models.URLField(max_length=1500)
    employment_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title

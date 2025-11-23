from django.db import models

class TimeStampedModel(models.Model):
    """
    Una clase abstracta que añade campos de created_at y updated_at
    a los modelos que la hereden.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

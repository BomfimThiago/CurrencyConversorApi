import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        abstract = True

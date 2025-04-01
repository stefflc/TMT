from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class UUIDModel(models.Model):
    uuid = models.UUIDField(unique=True, primary_key=True, editable=False)
    
    class Meta:
        abstract = True
    
    @classmethod
    def get_by_id(cls, uuid: str):
        try:
            return cls.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return None


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class IsActiveModel(models.Model):
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

    # I assumed that "active" should change is_active to True and vice versa.
    # Not sure if this is part of the test, or some fun reverse convention I have not seen :)
    @classmethod
    def activate(cls, pk: int):
        activated = cls.objects.filter(pk=pk).update(is_active=True)
        return activated

    @classmethod
    def deactivate(cls, pk: int):
        deactivated = cls.objects.filter(pk=pk).update(is_active=False)
        return deactivated

class NameModel(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        abstract = True
    
    @classmethod
    def get_by_name(cls, name: str):
        return cls.objects.filter(name=name)


class UniqueNameModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    class Meta:
        abstract = True
        
    @classmethod
    def get_by_name(cls, name: str):
        try:
            return cls.objects.get(name=name)
        except ObjectDoesNotExist:
            return None
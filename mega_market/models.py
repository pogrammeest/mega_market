import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import uuid


class ShopUnit(MPTTModel):
    SHOP_UNIT_TYPE = (
        ('O', 'OFFER'),
        ('C', 'CATEGORY')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.TextField(blank=False, null=False)

    date = models.DateTimeField(blank=True, null=True)
    parentId = TreeForeignKey("ShopUnit", null=True, on_delete=models.CASCADE, blank=True, related_name='children')
    type = models.CharField(max_length=1, choices=SHOP_UNIT_TYPE)
    price = models.IntegerField(null=True)

    class MPTTMeta:
        order_insertion_by = ['-id']
        parent_attr = 'parentId'


class LogsShopUnit(models.Model):
    SHOP_UNIT_TYPE = (
        ('O', 'OFFER'),
        ('C', 'CATEGORY')
    )
    unit_id = models.UUIDField(blank=False, unique=False)
    name = models.TextField(blank=False, null=False)
    date = models.DateTimeField(blank=False, null=False)
    parentId = models.UUIDField(null=True, blank=True)
    type = models.CharField(max_length=1, choices=SHOP_UNIT_TYPE)
    price = models.IntegerField(null=True)

    class MPTTMeta:
        order_insertion_by = ['-id']


@receiver(post_save, sender=ShopUnit)
def on_create(sender, instance, created, **kwargs):
    inst = instance.__dict__
    if '_mptt_saved' in inst:
        LogsShopUnit.objects.create(
            unit_id=inst['id'],
            name=inst['name'],
            date=inst['date'],
            parentId=inst['parentId_id'],
            type=inst['type'],
            price=inst['price']
        )


@receiver(post_delete, sender=ShopUnit)
def on_delete(sender, instance, using, **kwargs):
    inst = instance.__dict__
    LogsShopUnit.objects.filter(unit_id=inst['id']).delete()

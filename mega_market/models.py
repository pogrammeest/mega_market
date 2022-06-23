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
    date = models.DateTimeField(blank=True, null=True )
    parentId = TreeForeignKey("ShopUnit", null=True, on_delete=models.CASCADE, blank=True, related_name='children')
    type = models.CharField(max_length=1, choices=SHOP_UNIT_TYPE)
    price = models.IntegerField(null=True)

    class MPTTMeta:
        order_insertion_by = ['-id']
        parent_attr = 'parentId'



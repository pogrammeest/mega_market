import math
import uuid

from rest_framework import serializers
from mega_market.models import ShopUnit, LogsShopUnit
from django.db import transaction


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if data in (val, key):
                return key
        self.fail('invalid_choice', input=data)


class UpDateStruct:
    def update_tree_struct(self, instance, pre_inst=None):
        if instance.get_descendants(include_self=False):
            instance.price = 0
            count = 0
            for child in instance.get_descendants(include_self=False):
                if not child.get_children():
                    if child.price is not None:
                        instance.price += child.price
                    count += 1
            if pre_inst:
                instance.date = pre_inst.date
            if instance.price:
                instance.price = math.floor(instance.price / count) if count else None
            else:
                instance.price = None
        elif instance.type == 'C':
            instance.price = None

        instance.save()
        if instance.parentId:
            self.update_tree_struct(instance.parentId, instance)


class ShopUnitSerializer(serializers.ModelSerializer, UpDateStruct):
    type = ChoiceField(choices=ShopUnit.SHOP_UNIT_TYPE)
    date = serializers.SerializerMethodField()

    class Meta:
        model = ShopUnit
        fields = ['id', 'name', 'parentId', 'type', 'date', 'price']
        extra_kwargs = {
            'id': {'validators': []},
            'parentId': {'validators': []},
        }
        read_only_fields = ('parentId',)
        validators = []

    @staticmethod
    def get_date(obj):
        return obj.date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    def validate(self, data):
        return data

    def create(self, validated_data):
        inst, created = ShopUnit.objects.update_or_create(id=validated_data['id'], defaults={**validated_data})
        self.update_tree_struct(inst)
        return inst


class ItemsSerializer(serializers.Serializer, UpDateStruct):
    updateDate = serializers.DateTimeField()
    items = serializers.ListField(child=ShopUnitSerializer())

    class Meta:
        fields = ['updateDate', 'items']
        extra_kwargs = {'items': {'validators': []}, 'updateDate': {'write_only': True}}
        validators = []
        read_only_fields = ('items',)

    def code_400(self, field, message):
        raise serializers.ValidationError({'field': field, 'message': message})

    @staticmethod
    def id_validate(id):
        if isinstance(id, uuid.UUID):
            return id
        try:
            id = uuid.UUID(id, version=4)
        except ValueError:
            raise serializers.ValidationError({'code': 400, 'message': 'Validation Failed'})
        return id

    def validate(self, data):
        # ----- Init -----
        updated_date = data.get('updateDate')
        items = data.get('items')
        req_data = self.context['req'].data['items']
        previous_obj = {}
        # ----- Preparatory data, update and validate for id's -----
        cnt = 0
        for item in items:
            item.update({'date': updated_date})
            item.update({'parentId': req_data[cnt]['parentId']})
            item.update({'price': item.get('price', None)})
            self.id_validate(item['id'])
            if item['parentId'] is not None and not isinstance(item['parentId'], uuid.UUID):
                item['parentId'] = self.id_validate(item['parentId'])
            previous_obj[item['id']] = item
            cnt += 1
        # ----- Validate -----
        for item in items:
            query_set = ShopUnit.objects.filter(id=item['parentId'])
            if item['parentId'] is not None:
                if not query_set and item['parentId'] not in previous_obj.keys():
                    self.code_400('parentId', 'no such parent in DB or in request')
                elif query_set:  # if in base
                    parent = query_set.first()
                    if parent.type == 'O' or \
                            (item['type'] == 'C' and item['price'] is not None) or \
                            (item['type'] == 'O' and (item['price'] is None or item['price'] <= 0)):
                        self.code_400('parentId or price', 'not valid')
                elif str(item['parentId']) in previous_obj:  # if in list req
                    parent = previous_obj[str(item['parentId'])]
                    if (parent['type'] == 'OFFER') or \
                            (item['type'] == 'CATEGORY' and item['price'] is not None) or \
                            (item['type'] == 'OFFER' and (item['price'] is None or item['price'] <= 0)):
                        self.code_400('parentId or price', 'not valid')
                query_set = ShopUnit.objects.filter(id=item['id'])
                if query_set:
                    inst = query_set.first()
                    if inst.type != item['type']:
                        self.code_400('type', 'attempt to change the type')
        return data

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.get('items')
        for item in items:
            parent = item.get('parentId')
            if parent is not None:
                parent = ShopUnit.objects.get(id=parent)
                item.update({'parentId': parent})
            inst, created = ShopUnit.objects.update_or_create(id=item['id'], defaults={**item})
            self.update_tree_struct(inst)
        return validated_data


class ShopUnitDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUnit
        fields = ['id']
        extra_kwargs = {
            'id': {'validators': []},
        }


class ShopUnitNodesSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    type = ChoiceField(choices=ShopUnit.SHOP_UNIT_TYPE)
    date = serializers.SerializerMethodField()

    @staticmethod
    def get_children(obj):
        if obj.type == 'O':
            return None
        queryset = obj.get_children()
        if not queryset:
            return []
        children = ShopUnitNodesSerializer(queryset, many=True)
        return children.data

    # TODO: Getting a tree using mptt(get_children)

    @staticmethod
    def get_date(obj):
        return obj.date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    class Meta:
        model = ShopUnit
        fields = ['id', 'name', 'type', 'parentId', 'date', 'price', 'children']


class SalesSerializer(serializers.Serializer):
    items = serializers.ListField(child=ShopUnitSerializer())

    class Meta:
        fields = ['items']


class LogsShopUnitSerializer(serializers.ModelSerializer):
    type = ChoiceField(choices=ShopUnit.SHOP_UNIT_TYPE)
    date = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    @staticmethod
    def get_date(obj):
        return obj.date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    @staticmethod
    def get_id(obj):
        return obj.unit_id

    class Meta:
        model = LogsShopUnit
        fields = ['id', 'name', 'parentId', 'type', 'date', 'price']

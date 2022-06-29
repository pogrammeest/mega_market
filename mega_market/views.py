import json
import uuid
from datetime import timedelta, datetime
from dateutil import parser
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from mega_market.serializers import ShopUnitSerializer, ItemsSerializer, ShopUnitNodesSerializer, SalesSerializer
from rest_framework import status, viewsets
from mega_market.models import ShopUnit,LogsShopUnit
from rest_framework.decorators import action
from .examples import *


class ShopUnitViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Получение списка всех объектов shop unit.",
        responses={
            "200": openapi.Response(
                description="Список всех моделей",
                examples={"application/json": json.loads(json.dumps(ex_list))}
            ),
        })
    def list(self, request):
        queryset = ShopUnit.objects.all()
        serializer = ShopUnitSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(method='post', request_body=schema_import,
                         operation_description="Импорт новых товаров и/или категории. Товары/категории "
                                               "импортированные повторно"
                                               "обновляют текущие.",
                         responses={
                             200: openapi.Response(
                                 description='Вставка или обновление прошли успешно.',
                                 examples={"application/json": json.loads(json.dumps(ex_import_success))}
                             ),
                             400: openapi.Response(
                                 description='Невалидная схема документа или входные данные не верны.',
                                 examples={"application/json": json.loads(json.dumps(ex_no_valid))}
                             )})
    @action(detail=True, methods=['post'])
    def create(self, request):
        serializer = ItemsSerializer(data=request.data, context={'req': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 200, 'message': 'Вставка или обновление прошли успешно.'},
                            status=status.HTTP_200_OK)
        # print(serializer.data)
        # print(serializer.errors)
        return Response({'code': 400, 'message': 'Validation Failed'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Получить информацию об элементе по идентификатору. При получении информации о "
                              "категории также предоставляется информация о её дочерних элементах.",
        responses={
            200: openapi.Response(
                description='Информация об элементе.',
                examples={"application/json": json.loads(json.dumps(ex_node_success))}
            ),
            400: openapi.Response(
                description='Невалидная схема документа или входные данные не верны.',
                examples={"application/json": json.loads(json.dumps(ex_no_valid))}
            ),
            404: openapi.Response(
                description='Категория/товар не найден.',
                examples={"application/json": json.loads(json.dumps(ex_not_found))}
            ), })
    @action(detail=True, methods=['get'])
    def nodes(self, request, id=None):

        try:
            uuid.UUID(id, version=4)
        except ValueError:
            return Response({'code': 400, 'message': 'Validation Failed'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            inst = ShopUnit.objects.get(id=id)
        except ShopUnit.DoesNotExist:
            return Response({'code': 404, 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ShopUnitNodesSerializer(inst)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Удалить элемент по идентификатору. При удалении категории удаляются все дочерние "
                              "элементы.",
        responses={
            200: openapi.Response(
                description='Удаление прошло успешно.',
                examples={"application/json": json.loads(json.dumps(ex_delete_success))}
            ),
            400: openapi.Response(
                description='Невалидная схема документа или входные данные не верны.',
                examples={"application/json": json.loads(json.dumps(ex_no_valid))}
            ),
            404: openapi.Response(
                description='Категория/товар не найден.',
                examples={"application/json": json.loads(json.dumps(ex_not_found))}
            ), })
    def destroy(self, request, id=None):
        try:
            uuid.UUID(id, version=4)
        except ValueError:
            return Response({'code': 400, 'message': 'Validation Failed'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            inst = ShopUnit.objects.get(id=id)
            parent = inst.parentId
        except ShopUnit.DoesNotExist:
            return Response({'code': 404, 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        inst.delete()
        if parent is not None:
            item = ShopUnitSerializer(data=parent)
            item.update_tree_struct(ShopUnit.objects.get(id=parent.id))
        return Response({'code': 200, 'message': 'Удаление прошло успешно.'}, status=status.HTTP_200_OK)

    @staticmethod
    def iso_date_valid(dt_str):
        try:
            datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except ValueError:
            return False
        return True

    @swagger_auto_schema(
        operation_description='Получить список товаров, цена которых была обновлена за последние 24 часа включительно',
        properties={
            'date': openapi.Schema(type=openapi.TYPE_STRING, description='string', example="2022-02-01T12:00:00.000Z"),
        },
        responses={
            200: openapi.Response(
                description='Список товаров, цена которых была обновлена.',
                examples={"application/json": json.loads(json.dumps(ex_sales_success))}
            ),
            400: openapi.Response(
                description='Невалидная схема документа или входные данные не верны.',
                examples={"application/json": json.loads(json.dumps(ex_no_valid))}
            )},
        manual_parameters=[
            openapi.Parameter('date', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Дата и время запроса в формате ISO 8601.',
                              example="2022-02-01T12:00:00.000Z")
        ])
    @action(detail=True, methods=['get'])
    def sales(self, request):
        if 'date' in request.query_params.keys():
            date = request.query_params['date']
            if self.iso_date_valid(date):
                date = parser.parse(date)
                query_set = ShopUnit.objects.filter(date__gte=date - timedelta(hours=24), date__lte=date)
                serializer = SalesSerializer({'items': query_set})
                return Response(serializer.data)
        return Response({'code': 400, 'message': 'Validation Failed'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def statistic(self, request, id):
        try:
            ShopUnit.objects.get(id=id)
        except ShopUnit.DoesNotExist:
            return Response({'code': 404, 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        if 'dateStart' and 'dateEnd' in request.query_params.keys():
            date_start = request.query_params['dateStart']
            date_end = request.query_params['dateEnd']

            if self.iso_date_valid(date_start) and self.iso_date_valid(date_end):
                date_start = parser.parse(date_start)
                date_end = parser.parse(date_end)
                query_set = LogsShopUnit.objects.filter(unit_id=id, date__gte=date_start, date__lt=date_end)
                serializer = SalesSerializer({'items': query_set})
                return Response(serializer.data)
            else:
                return Response({'code': 400, 'message': 'Validation Failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            query_set = LogsShopUnit.objects.filter(unit_id=id)
            serializer = SalesSerializer({'items': query_set})
            return Response(serializer.data)

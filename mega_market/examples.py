from drf_yasg import openapi

ex_list = [
    {
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "name": "Товары",
        "parentId": None,
        "type": "CATEGORY",
        "date": "2022-02-01T12:00:00.000Z",
        "price": 89999
    },
    {
        "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
        "name": "Смартфоны",
        "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "type": "CATEGORY",
        "date": "2022-02-01T12:00:00.000Z",
        "price": 89999
    },
    {
        "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
        "name": "Xomiа Readme 10",
        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
        "type": "OFFER",
        "date": "2022-02-01T12:00:00.000Z",
        "price": 100000
    },
    {
        "id": "863e1a7a-1304-42ae-943b-179184c077e3",
        "name": "jPhone 13",
        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
        "type": "OFFER",
        "date": "2022-02-01T12:00:00.000Z",
        "price": 79999
    }]
ex_no_valid = {
    "code": 400,
    "message": "Validation Failed"
}
ex_not_found = {'code': 404, 'message': 'Item not found'}
ex_import_success = {
    "code": 200,
    "message": "Вставка или обновление прошли успешно."
}
ex_node_success = {
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "name": "Товары",
    "type": "CATEGORY",
    "parentId": None,
    "date": "2022-02-01T12:00:00.000Z",
    "price": 89999,
    "children": [
        {
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "name": "Смартфоны",
            "type": "CATEGORY",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "date": "2022-02-01T12:00:00.000Z",
            "price": 89999,
            "children": [
                {
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "name": "Xomiа Readme 10",
                    "type": "OFFER",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "date": "2022-02-01T12:00:00.000Z",
                    "price": 100000,
                    "children": None
                },
                {
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "name": "jPhone 13",
                    "type": "OFFER",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "date": "2022-02-01T12:00:00.000Z",
                    "price": 79999,
                    "children": None
                }
            ]
        }
    ]
}

ex_delete_success = {
    "code": 200,
    "message": "Удаление прошло успешно."
}
ex_sales_success = {
    "items": [
        {
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "name": "Товары",
            "parentId": None,
            "type": "CATEGORY",
            "date": "2022-02-01T12:00:00.000Z",
            "price": 89999
        },
        {
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "name": "Смартфоны",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "type": "CATEGORY",
            "date": "2022-02-01T12:00:00.000Z",
            "price": 89999
        },
        {
            "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
            "name": "Xomiа Readme 10",
            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "type": "OFFER",
            "date": "2022-02-01T12:00:00.000Z",
            "price": 100000
        },
        {
            "id": "863e1a7a-1304-42ae-943b-179184c077e3",
            "name": "jPhone 13",
            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "type": "OFFER",
            "date": "2022-02-01T12:00:00.000Z",
            "price": 79999
        }
    ]
}
schema_import = openapi.Schema(
    title="ShopUnitImportRequest",
    type=openapi.TYPE_OBJECT,
    properties={
        'items': openapi.Schema(type=openapi.TYPE_ARRAY, description='Импортируемые элементы', nullabale=False,
                                items=openapi.Schema(title="ShopUnitUmport", type=openapi.TYPE_OBJECT,
                                                     required=['id', 'name', 'type'],
                                                     properties={
                                                         'id': openapi.Schema(type=openapi.TYPE_STRING,
                                                                              description='Уникальный идентификатор',
                                                                              format=openapi.FORMAT_UUID,
                                                                              nullabale=False,
                                                                              example="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"),
                                                         'name': openapi.Schema(type=openapi.TYPE_STRING,
                                                                                description='Имя элемента.',
                                                                                nullabale=False, example="Товары"),
                                                         'parentId': openapi.Schema(type=openapi.TYPE_STRING,
                                                                                    description='Уникальный идентификатор',
                                                                                    format=openapi.FORMAT_UUID,
                                                                                    nullabale=True,
                                                                                    example="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"),
                                                         'price': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                                 description='Целое число, для категорий поле должно содержать null.',
                                                                                 nullabale=True, example=89999),
                                                         'type': openapi.Schema(type=openapi.TYPE_STRING,
                                                                                description='Тип элемента - категория или товар',
                                                                                example='CATEGORY',
                                                                                enum=['OFFER', 'CATEGORY'],
                                                                                nullabale=False),
                                                     }
                                                     )
                                ),
        'updateDate': openapi.Schema(type=openapi.TYPE_STRING, description='Invoice date',
                                     example="2022-02-01T12:00:00.000Z", format="YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"),

    }
)

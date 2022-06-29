from django.urls import path, include
from mega_market import views
from rest_framework.routers import DefaultRouter,SimpleRouter

shop_unit_list = views.ShopUnitViewSet.as_view({'get': 'list'})
shop_unit_import = views.ShopUnitViewSet.as_view({'post': 'create'})
shop_unit_node = views.ShopUnitViewSet.as_view({'get': 'nodes'})
shop_unit_delete = views.ShopUnitViewSet.as_view({'delete': 'destroy'})
shop_unit_sales = views.ShopUnitViewSet.as_view({'get': 'sales'})
shop_unit_statistic = views.ShopUnitViewSet.as_view({'get': 'statistic'})
router = DefaultRouter(trailing_slash=False)


urlpatterns = [
    path('list', shop_unit_list),
    path('imports', shop_unit_import),
    path('nodes/<str:id>', shop_unit_node),
    path('nodes/<str:id>/statistic', shop_unit_statistic),
    path('delete/<str:id>', shop_unit_delete),
    path('sales', shop_unit_sales),
    path('', include(router.urls)),
]

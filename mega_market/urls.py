from django.urls import path, include
from mega_market import views
<<<<<<< HEAD
from rest_framework.routers import DefaultRouter, SimpleRouter
=======
from rest_framework.routers import DefaultRouter,SimpleRouter
>>>>>>> 245dbcc359be52adecc83ec1af83f3e4ada97bca

shop_unit_list = views.ShopUnitViewSet.as_view({'get': 'list'})
shop_unit_import = views.ShopUnitViewSet.as_view({'post': 'create'})
shop_unit_node = views.ShopUnitViewSet.as_view({'get': 'nodes'})
shop_unit_delete = views.ShopUnitViewSet.as_view({'delete': 'destroy'})
shop_unit_sales = views.ShopUnitViewSet.as_view({'get': 'sales'})
<<<<<<< HEAD
shop_unit_statistic = views.ShopUnitViewSet.as_view({'get': 'statistic'})
router = DefaultRouter(trailing_slash=False)

=======

router = DefaultRouter(trailing_slash=False)


>>>>>>> 245dbcc359be52adecc83ec1af83f3e4ada97bca
urlpatterns = [
    path('list', shop_unit_list),
    path('imports', shop_unit_import),
    path('nodes/<str:id>', shop_unit_node),
    path('delete/<str:id>', shop_unit_delete),
    path('sales', shop_unit_sales),
    path('', include(router.urls)),
<<<<<<< HEAD
    path('node/<str:id>/statistic', shop_unit_statistic),
=======
>>>>>>> 245dbcc359be52adecc83ec1af83f3e4ada97bca
]

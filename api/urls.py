from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ListProduct, ProductDetailView, ProductCreateView,AddToCartView, CartViewSet

router = DefaultRouter()
router.register('cart',CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
    path('product-list', ListProduct.as_view(), name='list'),
    path('product-create', ProductCreateView.as_view(), name='create'),
    path('product-details/<int:pk>/', ProductDetailView.as_view(), name='details'),
    # path('cart/', AddToCartView.as_view(), name='cart'),

    path('cart/<int:pk>/list_cart_items/',CartViewSet.as_view({'get': 'list'}), name='list_cart_items'),

]
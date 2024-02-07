from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Product, Cart, CartProduct
from .serializer import ProductSerializer, CartSerializer
from rest_framework import generics, status, viewsets, permissions
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action



# Create your views here.

class ListProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get(self, request):
    #     queryset = self.get_queryset()
    #     serializer = ProductSerializer(queryset,many=True)
    #     return Response(serializer.data)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_object()
    #     if queryset is None:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     serializer = ProductSerializer(queryset, many=False)
    #     return Response(serializer.data)

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AddToCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



    #
    # def post(self,request):
    #     if not request.user.is_authenticated:
    #         return Response({'error': 'user is not authenticted'},status=status.HTTP_401_UNAUTHORIZED)
    #
    #     product_id = request.data.get('product_id')
    #     quantity = request.data.get('quantity')
    #
    #     try:
    #         product = Product.objects.get(pk=product_id)
    #         cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    #
    #         if not created:
    #             cart_item.quantity += quantity
    #             cart_item.save()
    #
    #         serializer = CartSerializer(cart_item)
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)
    #     except ObjectDoesNotExist:
    #         return Response({'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
    #
    # def get(self, request):
    #     cart_items = Cart.objects.filter(user=request.user)
    #     serializer = CartSerializer(cart_items, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False,methods=['get'])
    def my_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


    @action(detail=False,methods=['Post'])
    def add_to_cart(self, request):
        cart, created = Cart.objects.get_or_created(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity',1))


        try:
            product = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            return Response({'error':'Product not found'},status=status.HTTP_404_NOT_FOUND)
        cart_item, created = CartProduct.objects.get_or_create(cart=cart,product=product)
        cart_item.quantity += quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False,methods=['post'])
    def updatecart(self,request):
        cart_item_id = request.data.get('cart_item_id')
        quantity = int(request.data.get('quantity',1))

        try:
            cart_item = CartProduct.objects.get(pk=cart_item_id)
        except CartProduct.DoesNotExist:
            return Response({'eroor':'Cart item not found'},status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart_item.cart)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def remove_from_cart(self, request):
        cart_item_id = request.data.get('cart_item_id')

        try:
            cart_item = CartProduct.objects.get(pk=cart_item_id)
        except CartProduct.DoesNotExist:
            return Response({'error':'Cart item not found'},status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()

        # serializer = CartSerializer(cart_item.cart)
        return Response("item deleted")







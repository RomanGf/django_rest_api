from os import sep
import re
from wsgiref import validate
from django.http import request
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from api.mixins import StaffEditorPermisisionsMixin, UserQuerySetMixin

from .models import Product
from .serializers import ProductSerializers


class ProductListCreateAPIView(
    UserQuerySetMixin,
    generics.ListCreateAPIView,
    StaffEditorPermisisionsMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def perform_create(self, serializer):
        # print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title

        serializer.save(user=self.request.user ,content=content)

    # def get_queryset(self, *args, **kwargs):
    #     qs =super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     # print(request.user)
    #     return qs.filter(user=request.user)

product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(
    UserQuerySetMixin,
    generics.RetrieveAPIView,
    StaffEditorPermisisionsMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
    UserQuerySetMixin,
    generics.UpdateAPIView,
    StaffEditorPermisisionsMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(
    UserQuerySetMixin,
    generics.DestroyAPIView,
    StaffEditorPermisisionsMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

product_delete_view = ProductDestroyAPIView.as_view()

# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers

# product_List_view = ProductListAPIView.as_view()

class CreateApiView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
    ):

    pass 

class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):

    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'

    def get(self, request, pk=None, *args, **kwargs): 
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = ' this is a single view doing cool stuf'
        serializer.save(content=content)

product_mixin_view = ProductMixinView.as_view()


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == 'GET':
        if pk is not None :
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializers(obj, many=False).data
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializers(queryset, many=True).data
        return Response(data)
    if method == 'POST':
        serializer = ProductSerializers(data = request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title

            serializer.save(content=content)
            return Response(serializer.data)
        return Response({'invalid': 'not good data'}, status=400)
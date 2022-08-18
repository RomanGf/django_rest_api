from re import T
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view


from products.models import Product
from products.serializers import ProductSerializers


@api_view(['POST'])
def api_home(request, *args, **kwargs):
    serializers = ProductSerializers(data = request.data)
    if serializers.is_valid(raise_exception=True):
        return Response(serializers.data)
    return Response({'invalid': 'not good data'}, status=400)

# @api_view(['GET'])
# def api_home(request, *args, **kwargs):
#     """
#     DRF API  View
#     """
#     instance = Product.objects.all().order_by('?').first()
#     data = {}
#     if instance:
#         data = ProductSerializers(instance).data
#     return Response(data)
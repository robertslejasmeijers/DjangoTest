from rest_framework.serializers import ModelSerializer
from marga.models import Product


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields =  ["name", "link_to_picture", "store", "user"]
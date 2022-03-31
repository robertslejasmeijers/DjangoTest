from rest_framework.serializers import ModelSerializer
from marga.models import Product


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields =  ["name", "price", "price_old", "price_per_unit", "link_to_picture", "date_time_grab", "store_id", "discount_period"]
from rest_framework.serializers import ModelSerializer
from marga.models import Products


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields =  ["name", "price", "price_old", "price_per_unit", "link_to_picture", "date_time_grab", "store_id", "discount_period"]
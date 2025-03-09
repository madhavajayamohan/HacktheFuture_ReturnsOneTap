from rest_framework import serializers
from .models import ProductCondition, Products, Customer, OrderHistory, ReturnRequest

class ProductConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCondition
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = '__all__'

class ReturnRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = '__all__'

class ProductEvaluationSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    image = serializers.ImageField()
    text = serializers.TextField()

class ReturnSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    image = serializers.ImageField()
    text = serializers.TextField()
    refund_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    condition = serializers.CharField(max_length=50, choices=ReturnRequest.ProductCondition.choices)
    ret_option = serializers.CharField(max_length=50, choices=ReturnRequest.ReturnOption.choices)

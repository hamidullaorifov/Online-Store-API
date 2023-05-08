from rest_framework import serializers
from .models import Product,ProductItem,Review,Category
from users.serializers import UserSerializer


class ProductItemSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    class Meta:
        model = ProductItem
        fields = ('id','name','category','brand','price','discount','quantity')
        
    def get_quantity(self,obj):
        return obj.product.quantity if obj.product else 0
    def get_category(self,obj):
        return obj.category.name

class ProductSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer(required=True)
    class Meta:
        model = Product
        fields = ('product','quantity')
    def create(self, validated_data):
        product_data = validated_data.pop('product')
        product = ProductItem.objects.create(**product_data)
        return Product.objects.create(product=product, **validated_data)

class AddProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'quantity')
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id','product','owner','rate','description','created','updated')
        extra_kwargs = {'updated':{'read_only':True},'created':{'read_only':True}}
    def create(self, validated_data):
        review = Review.objects.filter(product=validated_data['product'],owner=validated_data['owner'])
        if review.exists():
            review = review.first()
            review.rate = validated_data['rate']
            review.description = validated_data['description']
            review.save()
        else:
            review = Review.objects.create(**validated_data)
        return review
class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'rate', 'description')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')
from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, default=[])

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions', 'products']


        # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for product in positions:
            StockProduct.objects.create(stock_id=stock.id,
                                        product_id=product['product'].id,
                                        quantity=product['quantity'],
                                        price=product['price'])
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions', [])


        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for product in positions:
            stock_product_list = StockProduct.objects.filter(stock=stock.id, product=product['product'])
            if stock_product_list:
                stock_product = stock_product_list[0]
                stock_product.quantity = product['quantity']
                stock_product.price = product['price']
                stock_product.save()
            else:
                StockProduct.objects.create(stock_id=stock.id,
                                            product_id=product['product'].id,
                                            quantity=product['quantity'],
                                            price=product['price'])
        return stock

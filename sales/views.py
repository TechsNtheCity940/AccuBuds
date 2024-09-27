from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Sale
from .serializers import SaleSerializer
from inventory.models import Product
import datetime

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    @action(detail=False, methods=['post'])
    def process_sale(self, request):
        # Extract sale information from request data
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        user_id = request.data.get('user_id')
        customer_id = request.data.get('customer_id')
        terminal_number = request.data.get('terminal_number')
        
        # Fetch the product
        product = Product.objects.get(id=product_id)

        # Ensure there is enough stock
        if product.quantity >= quantity:
            # Deduct the sold quantity from the stock
            product.quantity -= quantity
            product.save()

            # Log the sale
            sale = Sale.objects.create(
                product=product,
                quantity=quantity,
                total_price=product.recommended_sell_price * quantity,
                customer_id=customer_id,
                terminal_number=terminal_number,
                employee_id=user_id,
                sale_time=datetime.now()
            )
            sale.save()

            return Response({'status': 'Sale processed successfully'})
        else:
            return Response({'status': 'Not enough stock available'}, status=400)

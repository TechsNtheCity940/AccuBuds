from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Sale
from .serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    @action(detail=False, methods=['post'])
    def process_sale(self, request):
        """Atomic sale endpoint: validates stock, decrements inventory, logs sale."""
        product_id = request.data.get('product_id')
        patient_id = request.data.get('patient_id')
        user_id = request.data.get('user_id')
        quantity = request.data.get('quantity')
        terminal_number = request.data.get('terminal_number')

        # Validate required fields
        missing = [k for k, v in {
            'product_id': product_id,
            'patient_id': patient_id,
            'user_id': user_id,
            'quantity': quantity,
        }.items() if v is None]
        if missing:
            return Response(
                {'status': 'error', 'detail': f'missing fields: {missing}'},
                status=400,
            )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {'status': 'error', 'detail': 'quantity must be an integer'},
                status=400,
            )

        try:
            with transaction.atomic():
                from inventory.models import Product
                from patients.models import Patient
                from users.models import CustomUser

                product = Product.objects.select_for_update().get(id=product_id)
                if product.quantity < quantity:
                    return Response(
                        {'status': 'error', 'detail': 'not enough stock'},
                        status=400,
                    )
                patient = Patient.objects.get(id=patient_id)
                user = CustomUser.objects.get(id=user_id)

                sale = Sale.objects.create(
                    product=product,
                    patient=patient,
                    user=user,
                    quantity=quantity,
                    sale_price=product.recommended_sell_price,
                    terminal_number=terminal_number or '',
                )
                # Decrement stock via the model's save hook (atomic w/ the row lock)
                product.quantity -= quantity
                product.save(update_fields=['quantity'])

                return Response({
                    'status': 'ok',
                    'sale_id': sale.id,
                    'total': str(sale.sale_price * sale.quantity),
                })
        except Product.DoesNotExist:
            return Response({'status': 'error', 'detail': 'product not found'}, status=404)
        except Patient.DoesNotExist:
            return Response({'status': 'error', 'detail': 'patient not found'}, status=404)
        except CustomUser.DoesNotExist:
            return Response({'status': 'error', 'detail': 'user not found'}, status=404)

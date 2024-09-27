from rest_framework import viewsets
from patients.models import Patient
from patients.serializers import PatientSerializer
from django.shortcuts import render, redirect
from sales.models import Sale
from inventory.models import Product
from django.contrib import messages

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

def process_sale(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        patient_id = request.POST.get('patient')
        quantity = int(request.POST.get('quantity'))

        try:
            product = Product.objects.get(id=product_id)
            patient = Patient.objects.get(id=patient_id)

            if product.quantity < quantity:
                messages.error(request, 'Insufficient quantity in stock.')
            else:
                total_price = product.price * quantity
                sale = Sale.objects.create(
                    product=product,
                    patient=patient,
                    user=request.user,  # Assuming logged-in cashier
                    quantity=quantity,
                    total_price=total_price
                )
                
                # Update product quantity
                product.quantity -= quantity
                product.save()

                messages.success(request, 'Sale processed successfully!')
                return redirect('process_sale')
        except Product.DoesNotExist:
            messages.error(request, 'Product not found.')
        except Patient.DoesNotExist:
            messages.error(request, 'Patient not found.')

    # Display the form for product and patient selection
    products = Product.objects.all()
    patients = Patient.objects.all()

    return render(request, 'process_sale.html', {'products': products, 'patients': patients})
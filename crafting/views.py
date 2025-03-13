from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import DigitizingOrderForm
from .models import DigitizingOrder_Files

def digitizing_order(request):
    if request.method == 'POST':
        form = DigitizingOrderForm(request.POST, request.FILES)
        if form.is_valid():
            #order = form.save()
            file1 = request.FILES.get('file1')
            file2 = request.FILES.get('file2')
            
            if file1:
                print(file1)
                #DigitizingOrder_Files.objects.create(order=order,file=file1)
            if file2:
                print(file2)
                #DigitizingOrder_Files.objects.create(order=order,file=file2)
            print('Digitizing Order Save')
            return redirect('order_detail')
    else:
        form = DigitizingOrderForm()
    return render(request, 'digitizing_order.html', {'form': form})

# def patch_order(request):
#     if request.method == 'POST':
#         form = PatchOrderForm(request.POST, request.FILES)
#         if form.is_valid():
#             order = form.save()
#             return redirect('order_detail', order.id)
#     else:
#         form = PatchOrderForm()
#     return render(request, 'patch_order.html', {'form': form})

# def vector_order(request):
#     if request.method == 'POST':
#         form = VectorOrderForm(request.POST, request.FILES)
#         if form.is_valid():
#             order = form.save()
#             return redirect('order_detail', order.id)
#     else:
#         form = VectorOrderForm()
#     return render(request, 'vector_order.html', {'form': form})
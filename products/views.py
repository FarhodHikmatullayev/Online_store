from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View

from .forms import ProductForm
from .models import Product


class ProductListView(View):
    def get(self, request):
        products = Product.objects.order_by('-id')
        search_products = request.GET.get('q', '')
        if search_products:
            products = products.filter(name__icontains=search_products)

        page_size = request.GET.get('page_size', 20)
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ctx = {
            'object_list': page_obj,
        }

        return render(request, 'products/list.html', ctx)


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        ctx = {
            'product': product,
        }
        return render(request, 'products/detail.html', ctx)


class ProductCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProductForm()
        ctx = {
            'form': form,
        }
        return render(request, 'products/create.html', ctx)

    def post(self, request):
        form = ProductForm(data=request.POST, files=request.FILES)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            product = form.save(commit=False)
            print('user', request.user)
            product.user = request.user
            product.save()
            messages.success(request, 'Your product successfully created')
            return redirect(reverse('product:detail', kwargs={'pk': product.id}))
        messages.error(request, 'Your product didn\'t created')
        return render(request, 'products/create.html', ctx)


class ProductEditView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if not product.user == request.user:
            messages.warning(request, 'You haven\'t got permission for this product, you are not owner')
            return redirect('product:list')
        form = ProductForm(instance=product)
        ctx = {
            'product': product,
            'form': form,
        }
        return render(request, 'products/edit.html', ctx)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            form.save()
            messages.success(request, 'Your product successfully edited')
            return redirect(reverse('product:detail', kwargs={'pk': pk}))
        messages.error(request, 'Your product didn\'t edited')
        return render(request, 'products/edit.html', ctx)


class ProductDeleteView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if not product.user == request.user:
            messages.warning(request, 'You haven\'t got permission for this product, you are not owner')
            return redirect('product:list')
        ctx = {
            'product': product,
        }
        return render(request, 'products/delete.html', ctx)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        messages.success(request, 'Your product have successfully deleted')
        return redirect(reverse('product:list'))

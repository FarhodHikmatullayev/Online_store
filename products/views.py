import stripe
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from django.views.generic import TemplateView

from config import settings
from .forms import ProductForm, QuantityForm
from .models import Product, Cart, CartItem, Category


class ProductListView(View):
    def get(self, request):
        products = Product.objects.order_by('-id')
        search_name = request.GET.get('name', '')
        search_category = request.GET.get('category', '')
        search_price = request.GET.get('price')
        categories = Category.objects.all()
        if search_name:
            products = products.filter(name__icontains=search_name)
        if search_category:
            products = products.filter(category__title__icontains=search_category)
        if search_price:
            products = products.filter(price=search_price)
        page_size = request.GET.get('page_size', 20)
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ctx = {
            'categories': categories,
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


class ProductEditView(LoginRequiredMixin, View):
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


class ProductDeleteView(LoginRequiredMixin, View):
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


# this is for cart

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()

        ctx = {
            'cart': cart
        }
        return render(request, 'products/cart/cart.html', ctx)


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = QuantityForm()
        product = get_object_or_404(Product, id=pk)
        ctx = {
            'form': form,
            'product': product,
        }
        return render(request, 'products/cart/add_cart.html', ctx)

    def post(self, request, pk):
        form = QuantityForm(data=request.POST)

        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            product = get_object_or_404(Product, id=pk)
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += int(quantity)
            cart_item.save()
            messages.success(request, 'Product added to cart')
            return redirect('product:cart')
        ctx = {
            'form': form
        }
        messages.error(request, 'There are some problem, try again')
        return redirect(request, 'products/cart/add_cart.html', ctx)


# class CheckOutView(LoginRequiredMixin, View):
#     def get(self, request):
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         cart.cartitem_set.all().delete()
#         messages.success(request, 'Order placed successfully')
#         return redirect('product:cart')


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def get(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()

        line_items = []
        for cart_item in cart_items:

            item = {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(cart_item.product.price) * 100,
                    "product_data": {
                        "name": cart_item.product.name,
                        "description": cart_item.product.description,
                        # "images": [
                        #     request.build_absolute_uri(cart_item.product.image.url)
                        # ],
                    },
                },
                "quantity": cart_item.quantity,
            }
            if cart_item.product.image:
                image = [request.build_absolute_uri(cart_item.product.image.url)]
                item['price_data']['product_data']['images'] = image
            line_items.append(item)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        cart.cartitem_set.all().delete()
        messages.success(request, 'Order placed successfully')
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "products/cart/success.html"


class CancelView(TemplateView):
    template_name = "products/cart/cancel.html"

from django.shortcuts import render
from .models import Post


def detail_post(request, slug):
    detail_post = Post.objects.get(slug=slug)
    
    return render(request, 'blog-details.html', {'detail_post':detail_post})

def ecommerce_products(request):
    return render(request, 'ecommerce/products.html')

def ecommerce_product_detail(request):
    return render(request, 'ecommerce/product-details.html')


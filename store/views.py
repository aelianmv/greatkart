from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import product
# Create your views here.
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from django.db.models import Q


def store(request, category_slug=None):
    products=None
    categories = None

    if category_slug != None :
        categories = get_object_or_404(Category,slug = category_slug)
        products = product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        productcount=products.count()
    else :
        products = product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page) 

        productcount = products.count()
    
    
    context = {
        'pcount' : productcount,

        'productkey' : paged_product,
    }
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try : 
        single_product = product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product = single_product).exists()
        
    except Exception as e :
        raise e
    
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart
    }
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET :
        keyword = request.GET['keyword']
        if keyword:
            products = product.objects.filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            productcount = products.count()

    context = {
        'productkey' : products,
        'pcount' : productcount,
    }


    return render(request,'store/store.html',context)
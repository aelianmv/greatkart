from django.shortcuts import get_object_or_404, redirect, render
from store.models import product
from .models import Cart , CartItem 
from store.models import Variation
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request): 
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart

def add_cart(request,product_id):

    current_user = request.user
    Product = product.objects.get(id=product_id)   # product kittan aayit 

    #check user authenticated or not 
    if current_user.is_authenticated :
        product_variation = []
        if request.method=='POST':
            # color = request.POST['color']
            # size = request.POST['size']
        #return HttpResponse(color + "" + size)
        #return HttpResponse(color)
        #exit()
            for item in request.POST:
                key = item 
                value = request.POST[key]
                
                try :
                    variation = Variation.objects.get(Product=Product,variation_category__iexact=key , variation_value__iexact= value)
                    product_variation.append(variation)
                except:
                    pass 

                print(key,value)
        
        
        
        is_cart_item_exists = CartItem.objects.filter(product=Product,user=current_user).exists()  # 2st product p
            

        if is_cart_item_exists :
            cart_item = CartItem.objects.filter(product=Product, user=current_user)  # 1st product p
            #existing variation -- database 
            #current variation -- product variation 
            #item_id -- database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            print(ex_var_list)

            if product_variation in ex_var_list:
                    #increse hte cart item quantity 
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=Product,id=item_id)
                item.quantity +=1
                item.save()

            else:
                item = CartItem.objects.create(product=Product,quantity=1,user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        else:
            cart_item   = CartItem.objects.create(
                    product = Product, # 1st product p
                    quantity = 1,
                    user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()  
                cart_item.variations.add(*product_variation)
            cart_item.save()       #return HttpResponse(cart_item.product)
        
        return redirect('cart')
    #if the user is not authenticated
    else:

        product_variation = []
        if request.method=='POST':
            # color = request.POST['color']
            # size = request.POST['size']
        #return HttpResponse(color + "" + size)
        #return HttpResponse(color)
        #exit()
            for item in request.POST:
                key = item 
                value = request.POST[key]
                
                try :
                    variation = Variation.objects.get(Product=Product,variation_category__iexact=key , variation_value__iexact= value)
                    product_variation.append(variation)
                except:
                    pass 

                print(key,value)
        
        
        try :
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except  Cart.DoesNotExist :
            cart = Cart.objects.create(
                cart_id = _cart_id(request)

            )
        cart.save()
        is_cart_item_exists = CartItem.objects.filter(product=Product,cart=cart).exists()  # 2st product p
            

        if is_cart_item_exists :
            cart_item = CartItem.objects.filter(product=Product, cart=cart)  # 1st product p
            #existing variation -- database 
            #current variation -- product variation 
            #item_id -- database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            print(ex_var_list)

            if product_variation in ex_var_list:
                    #increse hte cart item quantity 
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=Product,id=item_id)
                item.quantity +=1
                item.save()

            else:
                item = CartItem.objects.create(product=Product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        else:
            cart_item   = CartItem.objects.create(
                    product = Product, # 1st product p
                    quantity = 1,
                    cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()  
                cart_item.variations.add(*product_variation)
            cart_item.save()       #return HttpResponse(cart_item.product)
        
        return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    
    Product = get_object_or_404(product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=Product,user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=Product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else :
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    
    Product = get_object_or_404(product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=Product,user=request.user,id=cart_item_id)
    else:
        cart= Cart.objects.get(cart_id=_cart_id(request))    
        cart_item = CartItem.objects.get(product=Product,cart=cart,id=cart_item_id)  # 1st product p
    cart_item.delete()
    return redirect('cart')
    
        


 


def cart(request,total=0,quantity=0,cart_items=None):
    cart = None
    try :
        tax=0
        grand_total=0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)    
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items :
            total+=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity 
        tax = (2*total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'cart' : cart,
        'cart_items' : cart_items,
        'quantity' : quantity,
        'total' : total,
        'grand_total' : grand_total,
        'tax':tax,
    } 
    return render(request,'store/cart.html',context)


@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    tax=0
    grand_total=0
    cart=None
    cart_items=[]
    try :
        # tax=0
        # grand_total=0
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)    
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items :
            total+=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity 
        tax = (2*total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'cart' : cart,
        'cart_items' : cart_items,
        'quantity' : quantity,
        'total' : total,
        'grand_total' : grand_total,
        'tax':tax,
    } 
    

    return render(request,'store/checkout.html',context)
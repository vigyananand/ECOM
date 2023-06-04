from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.shortcuts import render,redirect
from . models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import razorpay
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@login_required
def home(request):
    totalitem=0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
        wishlist= len(Wishlist.objects.filter(user=request.user))
    
    return render(request,'appp/home.html',locals())
@login_required
def about(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
        wishlist= len(Wishlist.objects.filter(user=request.user))
    return render(request,'appp/about.html',locals())
@login_required
def contact(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
        wishlist= len(Wishlist.objects.filter(user=request.user))
    return render(request,'appp/contact.html',locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values('title')
        return render(request,'appp/category.html',locals())
    
@method_decorator(login_required, name='dispatch')   
class CategoryTitle(View):
    def get(self,request,val):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(title=val)
        title= Product.objects.filter(category=product[0].category).values('title')
        return render(request,'appp/category.html',locals())   
    
@method_decorator(login_required, name='dispatch')
class ProductDetails(View):
    def get(self,request,pk):
       
        product=Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
       
        return render(request,'appp/productdetails.html',locals())  
      
  
class CustomerRegistrationView(View):
    def get(self, request):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
        form= CustomerRegistrationForm()
        return render(request,'appp/customerregistration.html',locals())  
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Succeessfully")
            # return redirect("accounts/login")

        else:
            messages.warning(request,"Invalid input")
        return render(request,'appp/customerregistration.html',locals()) 
    
@method_decorator(login_required, name='dispatch')   
class ProfileView(View):
    def get(self, request):
        totalitem=0

        wishlist=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
        form= CustomerProfileForm()
        return render(request,'appp/profile.html',locals()) 
        
    def post(self,request):
         form= CustomerProfileForm(request.POST)
         if form.is_valid():
             user= request.user
             name=form.cleaned_data['name']
             locality=form.cleaned_data['locality']
             city=form.cleaned_data['city']
             mobile=form.cleaned_data['mobile']
             zipcode=form.cleaned_data['zipcode']
             state=form.cleaned_data['state']
             reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,zipcode=zipcode,state=state)
             reg.save()
             messages.success(request,"Congratulation! form submitted succesfully")
         else:
             messages.warning(request,"Invallid user Data")

         return render(request,'appp/profile.html',locals()) 
@login_required
def address(request):
     
     add= Customer.objects.filter(user= request.user)
     totalitem=0
     wishlist=0
     if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
     return render(request,'appp/address.html',locals()) 


@method_decorator(login_required, name='dispatch')
class UpdateAddress(View):
    def get(self, request,pk):
         add= Customer.objects.get(pk=pk)
         form= CustomerProfileForm(instance=add)
         totalitem=0
         wishlist=0
         if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
         return render(request,'appp/updateAddress.html',locals()) 
    def post(self,request,pk):
         form= CustomerProfileForm(request.POST)
         if form.is_valid():
             add= Customer.objects.get(pk=pk)
             add.name=form.cleaned_data['name']
             add.locality=form.cleaned_data['locality']
             add.city=form.cleaned_data['city']
             add.mobile=form.cleaned_data['mobile']
             add.zipcode=form.cleaned_data['zipcode']
             add.state=form.cleaned_data['state']
             
             add.save()
             messages.success(request,"Congratulation! Address Updated succesfully")
         else:
             messages.warning(request,"Invallid user Data")

         return redirect("address")
    
@login_required       
def add_to_cart(request):
    user = request.user
    product_id= request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    user = request.user
    cart =Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
        totalamount = amount + 20
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
    return render(request,'appp/addcart.html',locals())

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount+value
        totalamount = famount+20
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency":"INR", "receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_LsKFleEBrjo32Y', 'entity': 'order', 'amount': 108200, 'amount_paid': 0, 'amount_due': 108200, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1684674911}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status = order_status

            )
            payment.save()
        return render(request,'appp/checkout.html',locals())
    
@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user = request.user
    # user_id=request.GET.get('cust_id')
    customer=Customer.objects.get(id=cust_id)
      
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
     totalitem=0
     wishlist=0
     if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
     order_placed = OrderPlaced.objects.filter(user=request.user)
     return render(request, 'appp/orders.html',locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)  & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount= amount+value
        totalamount= amount+20
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)  & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount= amount+value
        totalamount= amount+20
        data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount
        }
        return JsonResponse(data)
    
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)  & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount= amount+value
        totalamount= amount+20
        data={
           
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
@login_required    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product= Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data={
            'message':'Wishlist Added Successfully',

        }
        return JsonResponse(data)
    
@login_required   
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product= Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).delete()
        data={
            'message':'Wishlist Removed Successfully',

        }
        return JsonResponse(data)
    
@login_required   
def search(request):
    query = request.GET['search']
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
            wishlist= len(Wishlist.objects.filter(user=request.user))
    product= Product.objects.filter(Q(title__icontains=query))
    return render(request, "appp/search.html",locals())
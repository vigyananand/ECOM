from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm , MyPasswordResetForm, PasswordChangeForm, MyPasswordChangeForm, MySetPasswordForm


urlpatterns = [
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact, name="contact"),
    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("address/",views.address ,name="address"),
    path("category-title/<val>",views.CategoryTitle.as_view(),name="category-title"),
    path("product-detail/<int:pk>", views.ProductDetails.as_view(),name="product-detail"),
    path("updateAddress/<int:pk>", views.UpdateAddress.as_view(),name="updateAddress"),
    path("registration/",views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='appp/login.html', authentication_form=LoginForm) , name='login'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='appp/password_change.html', form_class=MyPasswordChangeForm , success_url='/passwordchangedone') , name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='appp/passwordchangesuccess.html' ) , name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    # password reset
    path('passwordreset/', auth_view.PasswordResetView.as_view(template_name='appp/passwordreset.html', form_class= MyPasswordResetForm) , name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='appp/password_reset_done.html') , name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='appp/password_reset_confirm.html', form_class= MySetPasswordForm) , name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='appp/password_reset_complete.html') , name='password_reset_complete'),

    #cart
    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),
    path('cart/',views.show_cart,name="showcart"),
    path('checkout/',views.checkout.as_view(),name="checkout"),
    path('paymentdone/',views.payment_done,name="paymentdone"),
    path('orders/',views.orders,name="orders"),
    path('search/',views.search,name='search'),


    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist),
    
    
]+static(settings. MEDIA_URL, document_root=settings.MEDIA_ROOT)
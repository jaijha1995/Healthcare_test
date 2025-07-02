from django.urls import path , re_path

from .views import CustomerViews, ListCustomerViews,LoginCustomer  , OTPView ,VerifyOTP , SendSMSAPIView , MobileVerifyOTP  , ForgotPasswordAPIView
from . import views

app_name = 'customer'
urlpatterns = [
    path('', CustomerViews.as_view()),
    path('<int:id>', CustomerViews.as_view()),
    path('org_id/''<int:org_id>', ListCustomerViews.as_view()),
    path('login', LoginCustomer.as_view()),
    path('otp', OTPView.as_view()),
    path('verifyotp', VerifyOTP.as_view()),
    path('mobileotp', SendSMSAPIView.as_view()),
    path('mobileverifyotp', MobileVerifyOTP.as_view()),
    path('forgetpassword', ForgotPasswordAPIView.as_view()),
    
]
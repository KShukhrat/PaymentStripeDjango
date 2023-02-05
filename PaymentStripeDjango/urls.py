from django.contrib import admin
from django.urls import path
from store.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", ProductLandingPageView.as_view(), name="landing-page"),
    path('create-checkoout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import Price, Product
from django.views.generic import TemplateView

stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductLandingPageView(TemplateView):
    template_name = "landing.html"
    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="test Product")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_SECRET_KEY
        })
        return context

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        domain = "https://yourdomain.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data':{
                        "currency": 'usd',
                        'unit_amount': 2000,
                        'product_data': {
                            'name': "Stubborn Attachmets",
                        },
                    },
                'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
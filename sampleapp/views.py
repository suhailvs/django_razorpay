import razorpay

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .models import Order

KEYS = {
    'test_id': 'rzp_test_uvBhuJZjsXdyn3',
    'test_secret': 'uEd4IHo8TrQMNwMP8qxLk7Gl',
    'live_id': "rzp_live_5ntl3qXAngLSso",
    'live_secret': "ZixHxaTePDrgrxTK4aDfFQZu"
}

razorpay_client = razorpay.Client(auth=(KEYS['test_id'], KEYS['test_secret']))

# Create your views here.
class Home(View):
    def get(self, request):
        data = {
            'amount': 100,
            'currency': 'INR',
            'payment_capture': 1        # Payment capture flag for auto capturing payment.
        }
        order = razorpay_client.order.create(data)
        # print(razorpay_client.order.payments(order['id']))
        Order.objects.create(razorpay_order_id=order['id'], amount = data['amount'])
        orders = Order.objects.all()
        return render(request,'home.html',
            {'orders': orders, 'order_id':order['id'],'amount': data['amount'], 'razorpayid': KEYS['test_id']})

    def post(self,request):
        order = Order.objects.get(razorpay_order_id=request.POST['razorpay_order_id'])
        try:
            razorpay_client.utility.verify_payment_signature(request.POST)
        except ValueError:
            return json.dumps('Signature Validatioon failed')

        order.is_paid = True
        order.razorpay_payment_id = request.POST['razorpay_payment_id']
        order.save()

        payment_id = request.POST['razorpay_payment_id']
        print(razorpay_client.order.payments(request.POST['razorpay_order_id']))
        print('-'*10)
        print(razorpay_client.payment.fetch(payment_id))
        return HttpResponse('Payment Success. PaymentID: {}'.format(payment_id))
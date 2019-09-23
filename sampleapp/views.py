import razorpay

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

KEY_ID = "rzp_live_5ntl3qXAngLSso"
KEY_SECRET = "ZixHxaTePDrgrxTK4aDfFQZu"
razorpay_client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

# Create your views here.
class Home(View):
    def get(self, request):
        data = {
            'amount': 100,
            'currency': 'INR',
            'receipt': 'test receipt',
            'payment_capture': 1
        }
        order = razorpay_client.order.create(data)
        return render(request,'home.html',
            {'order_id':order['id'],'amount': data['amount'], 'razorpayid': KEY_ID})

    def post(self,request):
        try:
            razorpay_client.utility.verify_payment_signature(request.POST)
        except ValueError:
            return json.dumps('Signature Validatioon failed')
        payment_id = request.POST['razorpay_payment_id']
        return HttpResponse('Payment Success. PaymentID: {}'.format(payment_id))
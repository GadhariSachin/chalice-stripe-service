from chalice import Chalice
import stripe
import jwt
import json
from chalice import CORSConfig

app = Chalice(app_name='stripeservice')

cors_config = CORSConfig(
    allow_origin='*',
)

# later move to env file for production
STRIPE_API_KEY = "sk_test_51HJgjtIWWRRN4vLS9KZkzohEUeyUnybXwdDr81jvngBIB698bC86RSikaCwIdtZMKFOlm1oI9dfpjiCWYeCXMXR100L8OziOrS"


@app.route('/payment', methods=['POST'],  cors = cors_config)
def chargeUser():
    stripe.api_key = STRIPE_API_KEY

    request_body = json.loads(app.current_request.raw_body)
    customer = stripe.Customer.create(
        email=request_body['email'],
        name=request_body['name'],
        address=request_body['address'],
        source=request_body['stripeToken']
    )

    print("Customer Created")
    print(customer.id)

    charge =  stripe.Charge.create(
        amount=request_body['amount'],
        customer=customer.id,
        currency="inr",
        description=request_body['description'],
    )
    
    print("Charge Created")
    print(charge)

    return {'status': 'success', 'charge':charge}

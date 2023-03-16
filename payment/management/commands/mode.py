import os
import braintree
from django.conf import settings

PLAN = "plan"

BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),  # commands
    "../",  # management
    "../",  # land
    "../",  # videoproj
)

PLAN_CONF_PATH = os.path.join(BASE_DIR, "braintree", "plan.json")

def get_braintree_gateway():
    if settings.BRAINTREE_PRODUCTION:
        braintree_env = braintree.Environment.Production
    else:
        braintree_env = braintree.Environment.Sandbox

    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree_env,
            merchant_id=os.environ.get("BRAINTREE_MERCHANT_ID"),
            public_key=os.environ.get("BRAINTREE_PUBLIC_KEY"),
            private_key=os.environ.get("BRAINTREE_PRIVATE_KEY"),
        )
    )
    return gateway

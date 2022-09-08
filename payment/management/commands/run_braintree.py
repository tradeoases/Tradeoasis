import os
import yaml
import json
import braintree
from django.conf import settings

from django.core.management.base import BaseCommand

PRODUCT = "product"
PLAN = "plan"

BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),  # commands
    "../",  # management
    "../",  # land
    "../",  # videoproj
)

PRODUCT_CONF_PATH = os.path.join(BASE_DIR, "braintree", "product.yml")
PLAN_CONF_PATH = os.path.join(BASE_DIR, "braintree", "plan.json")

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


class Command(BaseCommand):

    help = """
    Manages braintree Plans and Products
"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--create", "-c", choices=[PRODUCT, PLAN], help="Creates braintree plan"
        )
        parser.add_argument(
            "--list",
            "-l",
            choices=[PRODUCT, PLAN],
            help="List braintree products or plans",
        )

    def create_plan(self):
        with open(PLAN_CONF_PATH, "r") as f:
            data = json.load(f)
            for plan in data:
                result = gateway.plan.create(plan)

    def list_plan(self):
        ret = gateway.plan.all()
        print(ret)

    def create(self, what):
        if what == PRODUCT:
            self.create_product()
        else:
            self.create_plan()

    def list(self, what):
        if what == PRODUCT:
            self.list_product()
        else:
            self.list_plan()

    def handle(self, *args, **options):
        create_what = options.get("create")
        list_what = options.get("list")

        if create_what:
            # logger.debug(f"Create a {create_what}")
            self.create(create_what)
        elif list_what:
            # logger.debug(f"List {list_what}")
            self.list(list_what)

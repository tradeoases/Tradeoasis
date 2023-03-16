import yaml
import json

from django.core.management.base import BaseCommand
from payment import models as ManagerModels

from payment.management.commands import mode as braintree_config

class Command(BaseCommand):

    help = """
    Manages braintree Plans and Products
"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--create", "-c", choices=[braintree_config.PLAN], help="Creates braintree plan"
        )
        parser.add_argument(
            "--list",
            "-l",
            choices=[braintree_config.PLAN],
            help="List braintree products or plans",
        )

    def create_plan(self):
        with open(braintree_config.PLAN_CONF_PATH, "r") as f:
            data = json.load(f)
            for plan in data:
                if not ManagerModels.Feature.objects.filter(custom_id=plan.get("id")):
                    result = braintree_config.get_braintree_gateway().plan.create(plan)
                    if result.is_success:
                        feature = ManagerModels.Feature.objects.create(
                            custom_id = plan.get("id"),
                            name = plan.get("name"),
                            price = plan.get("price"),
                            description = plan.get("description"),
                            billing_frequency = plan.get("billing_frequency"),
                            currency_iso_code = plan.get("currency_iso_code")
                        )
                        if feature:
                            # log data
                            print(feature)
                    else:
                        print(result)

    def list_plan(self):
        ret = braintree_config.gateway.plan.all()
        print(ret)

    def create(self, what):
            self.create_plan()

    def list(self, what):
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

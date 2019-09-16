from .models import *

def create_plan_from_template(plan_template, cls, price=None, Description=None):
    plan = Plan(template=plan_template, cls=cls)
    plan.resources = plan_template.resources
    plan.remaining_resources = plan_template.resources
    plan.price = plan_template.default_price
    plan.subject = plan_template.subject
    plan.save()
    return True

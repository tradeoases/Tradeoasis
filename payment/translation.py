from modeltranslation.translator import register, TranslationOptions
from payment import models


@register(models.MembershipGroup)
class MembershipGroupTranslationOptions(TranslationOptions):
    fields = ("name", "description")

@register(models.MembershipPlan)
class MembershipGroupTranslationOptions(TranslationOptions):
    fields = ("name", "description")

class MembershipPlanTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(models.Feature)
class FeaturesTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.ModeOfPayment)
class ModeOfPaymentTranslationOptions(TranslationOptions):
    fields = ("name",)

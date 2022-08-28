from modeltranslation.translator import register, TranslationOptions
from payment import models


@register(models.MembershipPlan)
class MembershipPlanTranslationOptions(TranslationOptions):
    fields = ("name", "description", "price", "currency")


@register(models.Features)
class FeaturesTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.ModeOfPayment)
class ModeOfPaymentTranslationOptions(TranslationOptions):
    fields = ("name",)

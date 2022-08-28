from modeltranslation.translator import register, TranslationOptions
from manager import models


@register(models.Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(models.Showroom)
class ShowroomTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.Discussion)
class DiscussionTranslationOptions(TranslationOptions):
    fields = ("subject", "description")


@register(models.DiscussionReply)
class DiscussionReplyTranslationOptions(TranslationOptions):
    fields = ("description",)

from modeltranslation.translator import register, TranslationOptions
from supplier import models


@register(models.Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.ProductSubCategory)
class ProductSubCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("name", "description", "price", "currency")


@register(models.ProductTag)
class ProductTagTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("name", "description", "price", "currency")

from django.contrib import admin

# Register your models here.
from database_model.models import BusinessProfile, User, AuditTrail, ShowRoom

admin.site.site_header = "FORODEN MULTI VENDOR STORE"
admin.site.site_title = "FORODEN Admin Portal"
admin.site.index_title = "Welcome to FORODEN MULTI VENDOR STORE"

admin.site.register(User)
admin.site.register(BusinessProfile)
admin.site.register(AuditTrail)
admin.site.register(ShowRoom)


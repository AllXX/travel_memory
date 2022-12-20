from django.contrib import admin
from .models import Account,Memory,Geo,MemoryImage


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user','user_email','registerd_at')

    def user_email(self,obj):
        return obj.user.email
    user_email.short_description = 'メールアドレス'
    user_email.admin_order_field = 'user_email'



# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Memory)
admin.site.register(Geo)
admin.site.register(MemoryImage)


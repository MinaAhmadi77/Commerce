from django.contrib import admin
from .models import User,Categories,Bids,Comments,Listings,Watch
# Register your models here.

admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Categories)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(Watch)
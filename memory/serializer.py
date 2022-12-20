from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Account, Memory, Geo, Blog, Comment, Like

class AccountSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('user','image','birthplace','registerd_at')


class MemorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('date','place','account','memory_image','weather','feeling')
        


class GeoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('memory','lat','lng','ken')
        
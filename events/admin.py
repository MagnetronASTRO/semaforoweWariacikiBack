from django.contrib import admin
from .models import Event, EventMember, Category, Ticket, Image

admin.register([Event, EventMember, Category, Ticket, Image])

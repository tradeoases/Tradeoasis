from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.db.models import Q

from auth_app import models as AuthModels
from coms import models as ComsModels

from coms import tasks as ComsTasks

class InterClientChatInitView(View):
    def get(self, request, business_slug):
        business = AuthModels.ClientProfile.objects.filter(user=request.user)
        target_business = get_object_or_404(AuthModels.ClientProfile, slug=business_slug)
        if not business:
            return redirect(reverse("manager:dashboard"))
        else:
            business = business.first()

        # does one exist
        chat = ComsModels.InterClientChat.objects.filter(
            Q(initiator=business, participant=target_business)
            | Q(participant=business, initiator=target_business)
        )
        if chat:
            chat = chat.first()
        else:
            # create chat
            chat = ComsModels.InterClientChat.bjects.create(
                initiator = business,
                participant = target_business,
            )
            ComsTasks.notify_participant.delay(chat.pk, "Chat created")
        
        return redirect(reverse("buyer:messenger"))
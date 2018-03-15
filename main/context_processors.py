from django.conf import settings
from .models import Settings


def hackathon_info(request):
    return {
        "hack_has_started": Settings.hackathon_is_happening(),
        "hack_has_ended": Settings.hackathon_ended(),
        "hack_application_open": Settings.registration_is_open(),
        "hack_can_confirm": Settings.can_confirm(),
        "hack_settings": Settings.get(),
        "hackathon_name": settings.HACKATHON_NAME,
        "hackathon_email": settings.EMAIL_HOST_USER,
        "has_azure_passess": settings.AZURE_PASSES is not None,
        "helper": settings.HELPER,
        "rules": settings.EVENT_RULES,
        "chat": settings.CHAT,
        "root_url": settings.ROOT_URL,
        "max_team_size": settings.TEAM_MAX_SIZE,
        "ga_tracking_id": settings.GOOGLE_ANALYTICS,
        "data_url": settings.DATA_URL,
    }

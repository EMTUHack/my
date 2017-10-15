from django.conf import settings


def hackathon_info(request):
    return {
        "hack_has_started": settings.HACKATHON_STARTED,
        "hack_has_ended": settings.HACKATHON_ENDED,
        "hack_application_open": settings.APPLICATION_OPEN,
        "hackathon_name": settings.HACKATHON_NAME,
        "helper": settings.HELPER,
        "chat": settings.CHAT,
        "root_url": settings.ROOT_URL
    }

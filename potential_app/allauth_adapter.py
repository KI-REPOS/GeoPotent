# potential_app/allauth_adapter.py

from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp


class NoDbSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Use provider credentials from settings.SOCIALACCOUNT_PROVIDERS['google']['APP']
    and do NOT query the database for SocialApp.
    """

    def list_apps(self, request, provider=None, client_id=None):
        apps = []

        providers = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})

        if provider and provider in providers:
            app_cfg = providers[provider].get("APP")
            if app_cfg:
                app = SocialApp(
                    provider=provider,
                    name=f"{provider}-app",
                    client_id=app_cfg["client_id"],
                    secret=app_cfg["secret"],
                    key=app_cfg.get("key", ""),
                )
                # We don't save to DB; Allauth only needs the credentials.
                app.pk = None
                apps.append(app)

        return apps

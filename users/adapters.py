from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        self._populate_profile_from_suap(user, sociallogin)
        return user
    
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            self._populate_profile_from_suap(sociallogin.user, sociallogin)
    
    def _populate_profile_from_suap(self, user, sociallogin):
        extra = sociallogin.account.extra_data
        profile = user.profile
        profile.campus = extra.get('campus', '') or ''
        profile.matricula = extra.get('identificacao', '') or ''
        profile.tipo_vinculo = extra.get('tipo_usuario', '') or ''
        profile.foto_url = extra.get('foto', '') or ''
        profile.save()
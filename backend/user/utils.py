from user.models import UserProfile, UserSettings


def user_additional_models(request):
    """
    Creates additional user models ('UserSettings' and
    'UserProfile') for individual user settings and data.
    """
    settings_user = UserSettings.objects.filter(user=request.user).exists()
    profile_user = UserProfile.objects.filter(user=request.user).exists()
    if not settings_user:
        settings_user = UserSettings()
        settings_user.user = request.user
        settings_user.save()

    if not profile_user:
        profile_user = UserProfile()
        profile_user.user = request.user
        profile_user.save()
    return

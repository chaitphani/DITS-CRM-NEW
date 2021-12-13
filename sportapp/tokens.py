from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class UserActivateTokenMakerView(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )

account_activation_token = UserActivateTokenMakerView()

class UserActivateTokenMakerViewDashboard(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.register.email_confirmed)
        )

resend_activation_code = UserActivateTokenMakerViewDashboard

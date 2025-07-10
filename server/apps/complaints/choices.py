from django.db import models
from django.utils.translation import gettext_lazy as _


class ComplaintCategoryChoices(models.TextChoices):
    INAPPROPRIATE_CONTENT = 'inappropriate', _('Inappropriate content')
    SPAM = 'spam', _('Spam or advertisement')
    FRAUD = 'fraud', _('Fraud')
    OFFENSIVE = 'offensive', _('Offensive or hateful content')
    COPYRIGHT = 'copyright', _('Copyright infringement')
    MISLEADING = 'misleading', _('Misleading information')
    SCAM = 'scam', _('Scam or phishing')
    VIOLENCE = 'violence', _('Violent or threatening content')
    HARASSMENT = 'harassment', _('Harassment or bullying')
    DUPLICATE = 'duplicate', _('Duplicate or reposted content')
    FAKE_ITEM = 'fake_item', _('Fake or counterfeit item')
    WRONG_CATEGORY = 'wrong_category', _('Wrong category')
    PRICE_MANIPULATION = 'price_manipulation', _('Price manipulation')
    FAKE_PROFILE = 'fake_profile', _('Fake profile')
    IMPERSONATION = 'impersonation', _('Impersonation')
    OTHER = 'other', _('Other')

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import WalletLog

@receiver(post_save, sender=WalletLog)
@receiver(post_delete, sender=WalletLog)
def update_user_balance(sender, instance, **kwargs):
    """
    Updates the current_balance of the user whenever a WalletLog is created, updated, or deleted.
    """
    user_profile = instance.user
    
    # Calculate the new total balance
    total = user_profile.wallet_logs.aggregate(total=Sum('amount'))['total']
    
    # Update the user_profile.current_balance
    user_profile.current_balance = total if total is not None else 0.00
    user_profile.save(update_fields=['current_balance'])

from snapcleanup.azure.cli import AzureCli
from snapcleanup.entities import SubscriptionInfo


class SubscriptionService:

    @staticmethod
    def list_subscriptions() -> list[SubscriptionInfo]:
        cmd = ['account', 'subscription', 'list']
        subscriptions = AzureCli.run_cmd(cmd)

        list_subscriptions: list[SubscriptionInfo] = []
        if isinstance(subscriptions, list) and len(subscriptions) > 0:
            for subscription in subscriptions:
                list_subscriptions.append(
                    SubscriptionInfo (
                        subscription_id=subscription.get('subscriptionId'),
                        name=subscription.get('displayName')
                    )
                )

        return list_subscriptions
    

    @staticmethod
    def get_subscription(subscription_id: str) -> SubscriptionInfo | None:
        cmd = ['account', 'subscription', 'show' '--subscription-id', subscription_id]
        subscription = AzureCli.run_cmd(cmd)
        
        if subscription:
            return SubscriptionInfo (
                subscription_id=subscription.get('subscriptionId'),
                name=subscription.get('displayName')
            )

        return None
    

    @staticmethod
    def set_subscription(subscription_id: str) -> bool:
        cmd = ['account', 'set', '--subscription', subscription_id]
        result = AzureCli.run_cmd(cmd)
        if result:
            return True
        return False

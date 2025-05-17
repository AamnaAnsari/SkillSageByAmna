class PaymentGateway:
    def process_payment(self, user, amount):
        print(f"Simulating payment of ${amount} for {user.name}")
        return True

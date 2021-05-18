
class Payment():
    def __init__(self):
        self.option = "paypal"
        self.username = "Hans"
        self.password = "Hans"
        pass

    def selectPaymentOption(self):
        print("Payment option '{}' selected.".format(self.option))

    def waitOnRedirect(self):
        print("Wait on redirect.")

    def PaymentLogin(self):
        print("Login to payment provider")

    def FinishPayment(self):
        print("Payment finished!")

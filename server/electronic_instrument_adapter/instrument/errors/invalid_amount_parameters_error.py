class InvalidAmountParametersError(Exception):
    def __init__(self, sent, required):
        self.parameters_amount_sent = sent
        self.parameters_amount_required = required

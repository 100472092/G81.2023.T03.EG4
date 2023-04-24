from datetime import datetime
class OrderDelivered():
    def __init__(self,tracking_code):
        self.tracking_code = tracking_code
        self.delivery_day = datetime.utcnow().__str__()
class CardTextItem:
    def __init__(self, top_left, top_right, btm_left, btm_right, text, conf):
        self.top_left = top_left
        self.top_right = top_right
        self.btm_left = btm_left
        self.btm_right = btm_right
        self.text = text
        self.conf = conf
        self.is_examined = 0
        self.assigned_to = 0
        self.is_key = 0
        self.is_value = 0

    def __str__(self):
        return f"Text: {self.text}\ntop_left: {self.top_left}, top_right: {self.top_right}\n" \
               f"btm_left: {self.btm_left}, btm_right: {self.btm_right}\n" \
               f"examined: {self.is_examined}, assigned: {0 if self.assigned_to == 0 else 1} " \
               f"is_key: {self.is_key}, is_value: {self.is_value}"


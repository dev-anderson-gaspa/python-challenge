class FilterClass:
    criteria: dict

    def __init__(self, **criteria):
        self.criteria = criteria

    def compare(self, attr, product_value, filter_value):
        if attr == "name":
            return filter_value in product_value
        elif attr == "price":
            if filter_value is not None:
                return product_value >= filter_value
            return True
            
        elif attr == "best_seller":
            if filter_value is not None:
                return product_value == filter_value
            return True
        elif attr == "rating":
            if filter_value is not None:
                return product_value > filter_value
            return True
        else:
            return product_value == filter_value

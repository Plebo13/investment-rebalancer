class Investment:
    name = ""
    quantity = 0.0
    investment_sum = 0.0
    categories = list()

    def __str__(self):
        return self.name

    def add_category(self, category):
        self.categories.append(category)

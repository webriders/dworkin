

class FilterItem(object):
    name=""

    def __init__(self, is_multivalue = False):
        self.is_active = False
        self.is_multivalue = is_multivalue
        self.value = None
        self.user = None

    def filter_query(self, request, query):
        self.user = request.user
        if request.GET.has_key(self.name):
            self.is_active = True
            if self.is_multivalue:
                self.value = request.GET.getlist(self.name)
            else:
                self.value = request.GET.get(self.name)
            print self.__class__.__name__ + " ENABLED :" + self.name + "=" + str(self.value)
            query = self.filter(query)
            print self.__class__.__name__ + " Q :" + str(query.query)
        return query

    def filter(self, query):
        pass

    def get_context_data(self, filtered_ids):
        pass

class Filter(object):

    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def filter_query(self, request, query):
        for item in self.items:
            query = item.filter_query(request, query)
        return query

    def get_context_data(self, filtered_items):
        context = {}
        filtered_ids = [item.id for item in filtered_items]
        for item in self.items:
            item_context = item.get_context_data(filtered_ids)
            if item_context:
                context.update(item_context)
        return context

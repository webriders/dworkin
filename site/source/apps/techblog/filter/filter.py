
class FilterItem(object):
    name=""

    def __init__(self, is_multivalue=False, always_use=False):
        self.is_active = False
        self.is_multivalue = is_multivalue
        self.always_use = always_use
        self.value = None
        self.user = None

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
        self.load_from_request(request.GET)

        for item in self.items:
            item.user = request.user
            if item.is_active:
                query = item.filter(query)

        return query

    def get_context_data(self, filtered_items):
        context = {}
        filtered_ids = [item.id for item in filtered_items]
        for item in self.items:
            item_context = item.get_context_data(filtered_ids)
            if item_context:
                context.update(item_context)
        context["the_filter"] = self
        return context

    def load_from_request(self, request_data):
        for item in self.items:
            if item.always_use:
                item.is_active = True

            # load from request (first prio)
            if request_data.has_key(item.name):
                item.is_active = True
                if item.is_multivalue:
                    item.value = request_data.get(item.name).split(',')
                else:
                    item.value = request_data.get(item.name)

            # reset filter (show all :) )
            if request_data.has_key("all_" + item.name):
                item.is_active = False
                item.value = None

    def get_params(self):
        params = []
        for item in self.items:
            if item.value:
                params.append( (item.name, item.value) )
        return dict(params)


    def __unicode__(self):
        fstr = ""
        for item in self.items:
            fstr += "[Filter:%s enabled:%s value:%s] " % (item.name, str(item.is_active), str(item.value))
        return fstr

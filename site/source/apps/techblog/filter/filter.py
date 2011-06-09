class FilterItem(object):
    name=""

    def __init__(self, is_multivalue = False):
        self.is_active = False
        self.is_multivalue = is_multivalue
        self.value = None
        self.user = None

    def filter(self, query):
        pass

    def get_context_data(self, filtered_ids):
        pass

class Filter(object):

    def __init__(self, store_in_session = False):
        self.items = []
        self.store_in_session = store_in_session

    def add_item(self, item):
        self.items.append(item)

    def filter_query(self, request, query):
        self.load_from_request(request.GET, request.session)

        for item in self.items:
            item.user = request.user
            if item.is_active:
                query = item.filter(query)

        if self.store_in_session:
            self.save_to_session(request.session)
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

    def load_from_request(self, request_data, session):
        for item in self.items:
            # load from request (first prio)
            if request_data.has_key(item.name):
                item.is_active = True
                if item.is_multivalue:
                    item.value = request_data.getlist(item.name)
                else:
                    item.value = request_data.get(item.name)

            # load from session (second prio)
            elif self.store_in_session:
                if session.has_key(item.name):
                    item.is_active = True
                    if item.is_multivalue:
                        item.value = session.get(item.name)
                    else:
                        item.value = session.get(item.name)

            # reset filter (show all :) )
            if request_data.has_key("all_" + item.name):
                item.is_active = False
                item.value = None
                if self.store_in_session and session.has_key(item.name):
                    del session[item.name]


    def save_to_session(self, session):
        for item in self.items:
            if item.is_active:
                session[item.name] = item.value
            else:
                if session.has_key(item.name):
                    del session[item.name]


    def __unicode__(self):
        fstr = ""
        for item in self.items:
            fstr += "[Filter:%s enabled:%s value:%s] " % (item.name, str(item.is_active), str(item.value))
        return fstr

from django import template
import ttag

register = template.Library()


class AbstractFiltersTag(ttag.Tag):
    filter_obj = ttag.Arg()

    def output(self):
        raise NotImplementedError()

    def get_current_params(self, data):
        filter_obj = data.get('filter_obj')
        params = filter_obj.get_params()
        return params

    @staticmethod
    def toogle_item_in_items(item, items):
        if item:
            if items:
                items = set(items)

                if item in items:
                   items.remove(item)
                else:
                   items.add(item)

                items = list(items)
            else:
                items = [item]
        return items

    @staticmethod
    def make_url(params):
        params_str = '?'

        for key in params:
            params_str += key

            if params[key] != '':
                params_str += '='+unicode(params[key])
            params_str += '&'

        return params_str[:-1]

    @staticmethod
    def update_list_in_params(params, list_name, list_value):
        params = params.copy()
        if list_value:
           params[list_name] = ','.join(list_value)

        elif list_name in params:
           del params[list_name]

        return params


class UpdateFilters(AbstractFiltersTag):
    class Meta:
        name = "update_filters"

    page = ttag.IntegerArg(keyword=True, required=False)
    category = ttag.StringArg(keyword=True, required=False)
    tag = ttag.StringArg(keyword=True, required=False,)
    own = ttag.StringArg(keyword=True, required=False,)
    lang = ttag.StringArg(keyword=True, required=False,)

    all_own = ttag.IntegerArg(keyword=True, required=False)
    all_category = ttag.IntegerArg(keyword=True, required=False)
    all_tags = ttag.IntegerArg(keyword=True, required=False)
    all_langs = ttag.IntegerArg(keyword=True, required=False)
    all_author = ttag.IntegerArg(keyword=True, required=False)


    def output(self, data):
        params = self.get_current_params(data)

        for param_name in ('langs', 'page', 'own', 'all_own', 'all_author',):
            param_value = data.get(param_name)

            if param_value:
                params[param_name] = param_value

        params = self.add_or_remove_category(data, params)
        params = self.add_or_remove_tag(data, params)
        params = self.add_or_remove_lang(data, params)

        for param in params.copy():
            if param.startswith('all_'):
                par = param.replace('all_', '')
                if par in params:
                    del params[par]
                if param in params:
                    del params[param]
        return self.make_url(params)


    def add_or_remove_category(self, data, params):
        old_category = params.get('category')
        new_category =  data.get('category')

        if 'all_category' in data and old_category:
            del params['category']
            return params

        if new_category:
            if old_category == new_category:
                del params['category']
            else:
                params['category'] = new_category
        return params

    def add_or_remove_tag(self, data, params):
        tags = params.get('tags')

        if 'all_tags' in data and tags:
            del params['tags']
            return params

        tag = data.get('tag')
        tags = self.toogle_item_in_items(tag, tags)
        params = self.update_list_in_params(params, 'tags', tags)

        return params

    def add_or_remove_lang(self, data, params):
        langs = params.get('langs')

        if 'all_langs' in data and langs:
            del params['langs']
            return params

        lang = data.get('lang')
        langs = self.toogle_item_in_items(lang, langs)
        params = self.update_list_in_params(params, 'langs', langs)

        return params

register.tag(UpdateFilters)


class RemoveFilters(AbstractFiltersTag):
    class Meta:
        name = "remove_filter"

    filter_name = ttag.Arg()
    filter_value = ttag.Arg(required=False)
    filter_slug = ttag.Arg(required=False)

    def output(self, data):
        params = self.get_current_params(data)

        filter_name = data.get('filter_name')
        filter_slug = data.get('filter_slug')
        tags = params.get('tags')

        for param_name in ('own', 'category', ):
            if filter_name == param_name and param_name in params:
                del params[param_name]

        if filter_name == 'tag' and filter_slug in tags:
            tags = self.toogle_item_in_items(filter_slug, tags)

        params = self.update_list_in_params(params, 'tags', tags)
        return self.make_url(params)

register.tag(RemoveFilters)

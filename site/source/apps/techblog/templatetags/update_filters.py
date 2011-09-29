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

    def process_tag_in_tags(self, tag, tags):
        if tag:
            if tags:
                tags = set(tags)

                if tag in tags:
                   tags.remove(tag)
                else:
                   tags.add(tag)
            else:
                tags = set((tag,))
        return tags

    def make_url(self, params):
        params_str = '?'

        for key in params:
            params_str += key

            if params[key] != '':
                params_str += '='+unicode(params[key])
            params_str += '&'

        return params_str[:-1]


class UpdateFilters(AbstractFiltersTag):
    class Meta:
        name = "update_filters"

    page = ttag.IntegerArg(keyword=True, required=False)

    category = ttag.StringArg(keyword=True, required=False)
    tag = ttag.StringArg(keyword=True, required=False,)
    own = ttag.StringArg(keyword=True, required=False,)

    all_own = ttag.IntegerArg(keyword=True, required=False)
    all_category = ttag.IntegerArg(keyword=True, required=False)
    all_tags = ttag.IntegerArg(keyword=True, required=False)
    all_author = ttag.IntegerArg(keyword=True, required=False)


    def output(self, data):
        params = self.get_current_params(data)

        for param_name in ('page', 'own', 'all_own', 'all_author',):
            param_value = data.get(param_name)

            if param_value:
                params[param_name] = param_value

        params = self.add_or_remove_category(data, params)
        params = self.add_or_remove_tag(data, params)

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
        tags = self.process_tag_in_tags(tag, tags)

        if tags:
            params['tags'] = ','.join(tags)

        elif 'tags' in params:
            del params['tags']

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

        tags = params.get('tags')
        filter_name = data.get('filter_name')
        filter_slug = data.get('filter_slug')

        if filter_name == 'own' and 'own' in params:
            del params['own']

        if filter_name == 'category' and 'category' in params:
            del params['category']

        print filter_slug
        if filter_name == 'tag' and filter_slug in tags:
            tags = self.process_tag_in_tags(filter_slug, tags)

        #TODO: remove copypast
        if tags:
            params['tags'] = ','.join(tags)

        elif 'tags' in params:
            del params['tags']


        return self.make_url(params)

register.tag(RemoveFilters)

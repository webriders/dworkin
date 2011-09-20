from django import template
import ttag

register = template.Library()

class UpdateFilters(ttag.Tag):
    class Meta:
        name = "update_filters"

    filter_obj = ttag.Arg()

    page = ttag.IntegerArg(keyword=True, required=False)

    category = ttag.StringArg(keyword=True, required=False)
    tag = ttag.StringArg(keyword=True, required=False,)
    own = ttag.StringArg(keyword=True, required=False,)

    all_own = ttag.IntegerArg(keyword=True, required=False)
    all_category = ttag.IntegerArg(keyword=True, required=False)
    all_tags = ttag.IntegerArg(keyword=True, required=False)
    all_author = ttag.IntegerArg(keyword=True, required=False)


    def output(self, data):
        filter_obj = data.get('filter_obj')
        params = filter_obj.get_params()

        for param_name in ('page', 'category', 'own', 'all_own', 'all_category', 'all_author',):
            param_value = data.get(param_name)

            if param_value:
                params[param_name] = param_value

        params = self.add_or_remove_tag(data, params)
        
        for param in dict(params):
            if param.startswith('all_'):
                par = param.replace('all_', '')
                if par in params:
                    del params[par]

        return self.make_url_params(params)


    def add_or_remove_tag(self, data, params):
        tags = params.get('tags')

        if ('all_tags' in params or 'all_tags' in data) and tags:
            del params['tags']
            return params

        tag = data.get('tag')
        if tag:
            if tags:
                tags = set(tags)

                if tag in tags:
                   tags.remove(tag)
                else:
                   tags.add(tag)
            else:
                tags = set((tag,))

        if tags:
            params['tags'] = ','.join(tags)

        elif 'tags' in params:
            del params['tags']

        return params


    def make_url_params(self, params):
        params_str = '?'

        for key in params:
            params_str += key

            if params[key] != '':
                params_str += '='+unicode(params[key])
            params_str += '&'

        return params_str[:-1]


register.tag(UpdateFilters)

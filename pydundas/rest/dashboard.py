class DashboardApi:

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def get_view_data(self, dash_id):
        return self.session.get('dashboard/' + dash_id).json()

    def set_view_parameter(self, view_data, param_name, param_value):
        """
            Update the value of one view parameter, by name.
            Note that name is the *script name* not the friendly name.
            This is very limited as I could not find a good generic way to do it.
            Note that param_value must be the actual json value, ie. something like actual_value.param_name.
        """
        view_params = view_data['viewParameters']
        for vp in view_params:
            if vp['name'] == param_name:
                vp['parameterValue']['values'][0]['uniqueName'] = param_value
                break

        return view_data

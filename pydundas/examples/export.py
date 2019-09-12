from pydundas import Api, Session, creds_from_yaml

# Needs to be a non-api user
creds = creds_from_yaml('credential.yaml')
with Session(**creds) as d:
    api = Api(d)
    eapi = api.export()
    dapi = api.dashboard()

    # What id the dashboard root id?
    root_dir = api.project().getRootFolderIdForProject('project', 'dashboards')
    # Now where is the dashboard we are interested in?
    dash_dir = api.file().getFileInfo(root_dir, 'path/to/dashboard')
    # From the dashboard, get its relevant data.
    dash_id = dash_dir['id']
    dash_data = dapi.get_view_data(dash_id)

    # Could be of course pdf or something else.
    img_provider = api.constant().getIdByName("STANDARD_IMAGE_EXPORT_PROVIDER_ID")


    param_value = 'actual relevant value'
    param_name = 'script name of your prarameter'

    # Update the view data, which has default value for params, with the relevant values for this export.
    dash_data_with_param = dapi.set_view_parameter(
        view_data=dash_data,
        param_name=param_name,
        # Not the format here. It looks like it is required bu feels brittle for the long term.
        param_value=param_value + '.' + param_name
    )
    # This generates the export of the server.
    export_id = eapi.enqueue(
        provider_id=img_provider,
        view_id=dash_id,
        view_data=dash_data_with_param
    )
    # It can then be downloaded (or displayed with .show_image()).
    eapi.download(export_id, f'{param_value}.png', override=True)



class NonInteractiveUserError(Exception):
    pass


class ExportApi:
    """Uses the Api to export a dashboard."""

    # References:
    # https://www.dundas.com/support/developer/samples/integration/create-an-export-and-download-a-file
    # https://www.dundas.com/support/developer/script-library/export/create-an-image-export
    # https://www.dundas.com/support/developer/script-library/export/exporting-with-parameters

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def ensure_interactive_user(self):
        """An export can only be run by an interactive user. Check that."""
        if self.session.is_api_session():
            raise NonInteractiveUserError("To run export, you need a non-api user.")

    def enqueue_raw(self, raw_json):
        """
        Enqueue an export when the full json is given.
        """

        self.ensure_interactive_user()
        export_id = self.session.post('export', json=raw_json)
        # The returned ID is json, so between quotes which should be removed for future use.
        return export_id.text.replace('"', '')

    def enqueue(self, view_data, provider_id, view_id):
        """
        Enqueue an export based on its specification.
        View_id is the dashboard id.
        view_data is the data from the dashboard. Basically its full definition. See example.
        provider_id: image, pdf, other?
        """
        # Otherwise you'll get headers, footers, explore menu.
        view_data['initialViewOptions'] = 'viewonly'

        payload = {
            "ProviderId": provider_id,
            "ViewData": view_data,
            "ViewId": view_id,
            'ParameterValues': []
        }
        return self.enqueue_raw(payload)

    def download(self, export_id, local_path, override=False):
        """
        From an export_id, download it to a file.
        """
        data = self.session.get('/export/result/' + export_id)
        mode = 'wb' if override else 'wx'
        with open(local_path, mode=mode) as f:
            f.write(data.content)
        return True

    def show_image(self, export_id):
        """
        If the export is an image export, show it interactively.
        If not an image, expect some blowing up.
        """
        img = self.session.get('/export/result/' + export_id)
        from io import BytesIO
        from PIL import Image
        i = Image.open(BytesIO(img.content)).show()

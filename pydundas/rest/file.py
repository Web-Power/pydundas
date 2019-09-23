from requests import HTTPError


class DundasFileNotFoundError(Exception):
    pass


class FileApi:
    """Uses the Api to manipulate files."""

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def getFileInfo(self, parent_dir_id, path, parents=''):
        """
        Get a file, from its full path.
        The parents parameter is just a string accumulator to know where we are in the tree to display useful error
        messages.
        """
        root, sep, rest = path.partition('/')
        current = None
        try:
            current = self.session.post('File/Name', json={'FileName': root, 'ParentId': parent_dir_id}).json()
        except HTTPError as e:
            if e.response.status_code == 410:
                raise DundasFileNotFoundError("File '{}' in '{}' not found.".format(root, parents)) from None
            else:
                # No idea what could be the cause here.
                raise

        if not sep:
            return current
        else:
            new_parent = current['id']
            return self.getFileInfo(new_parent, rest, parents + '/' + root)

import pkg_resources


def load_description(package: str, path: str, filename: str):
    """
    This function loads a static description file.

    Parameters:
        package (str): Package name where file is located in
        path (str): Path within the package.
        filename (str): Name of file to load.

    Returns:
        str: Content of loaded file
    """
    with open(pkg_resources.resource_filename(
            package, f"{path}{filename}"), "r+") as file:
        return file.read()

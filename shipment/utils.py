def import_from_string(name):
    """
    Import a Python class from a string.
    """
    components = name.split('.')
    module = __import__(components[0])
    for component in components[1:]:
        module = getattr(module, component)
    return module

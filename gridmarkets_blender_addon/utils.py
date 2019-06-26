def get_unique_id(objects, attribute_name='id'):
    """ Returns an integer ID that has not been used by any other object in the provided list.

    :param objects: a list of existing objects that may or may not have an id attribute
    :type objects: list
    :param attribute_name: the attribute containing the id
    :type attribute_name: str
    :return: the new unique id
    :rtype: int
    """

    used_ids = []

    for object in objects:
        id = object.id

        if not isinstance(id, int):
            continue

        used_ids.append(id)

    # find a number which has not been used yet
    unused_id = 0
    while unused_id in used_ids:
        unused_id = unused_id + 1

    return unused_id


def create_unique_object_name(objects, attribute_name='name', name_prefix = ""):
    """ Creates a unique name of the form [name_prefix][x] where x is some unique positive integer.

    :param objects: the existing list of objects that this new name must not collide with. Objects in said list may or
                    may not have .name attributes or follow the provided naming scheme
    :type objects: list
    :param attribute_name: The name of the attribute which contains the objects name
    :type attribute_name: str
    :param name_prefix: a optional prefix to append before the unique number
    :type name_prefix: str
    :return: the unique name
    :rtype: str
    """

    prefix_length = len(name_prefix)

    # compile a list of used numeric integer suffixes
    used_suffixes = []
    for element in objects:

        if not hasattr(element, attribute_name):
            continue

        name = getattr(element, attribute_name)

        if not isinstance(name, str):
            continue

        if not name.startswith(name_prefix):
            continue

        element_suffix = name[prefix_length:]
        if element_suffix.isdigit():
            try:
                element_suffix = int(element_suffix)

                if element_suffix >= 0:
                    used_suffixes.append(element_suffix)

            except ValueError:
                pass

    # remove duplicates
    used_suffixes = list(set(used_suffixes))

    # sort
    used_suffixes.sort()

    # find a number which has not been used yet
    i = 0
    while i in used_suffixes:
        i = i+1

    return name_prefix + str(i)


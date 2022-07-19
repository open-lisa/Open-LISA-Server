from functools import reduce
import os


class FileManager:
    def __init__(self) -> None:
        # NOTE: this class could have CRUDs logic for OpenLISA files (pos process, clibs, etc)
        pass

    def list_directory_recursively(self, directory):
        # Src of as_dict calculation https://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
        as_dict = {}
        rootdir = directory.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, _, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(files)
            parent = reduce(dict.get, folders[:-1], as_dict)
            parent[folders[-1]] = subdir

        # transform as_dict to list (best for frontend rendering)
        base_key = list(as_dict.keys())[0]
        directory_as_list = self.__transform_directory_represented_as_dict_to_list(
            as_dict[base_key])
        return directory_as_list

    def __transform_directory_represented_as_dict_to_list(self, directory_dict={}):
        result = []
        keys = list(directory_dict.keys())
        keys_that_are_directories = sorted(
            filter(lambda k: type(directory_dict[k]) == dict, keys))
        keys_that_are_files = sorted(
            filter(lambda k: directory_dict[k] == None, keys))
        keys = keys_that_are_directories + keys_that_are_files
        for k in keys:
            if type(directory_dict[k]) == dict:  # it is a directory
                children = self.__transform_directory_represented_as_dict_to_list(
                    directory_dict[k])
                result.append({
                    "name": k,
                    "type": "directory",
                    "children": children
                })
            elif directory_dict[k] == None:  # it is a file
                result.append({
                    "name": k,
                    "type": "file",
                })
        return result

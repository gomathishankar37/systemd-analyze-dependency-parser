import argparse
from typing import Dict, List
 
#file_path = "full.dot"
ignore_color = ["dark blue", "red"]
legends_dict = {
    "black" : "Requires",
    "grey66": "Wants",
    "green": "After"
}
 
def depend_parser(dependencies: Dict[str, Dict[str, List[str]]], service_name: str, assoc_lst: List[str], flag: bool):
    """
    Parse dependencies for a given service and print the results.

    Args:
        dependencies (Dict[str, Dict[str, List[str]]]): The dictionary containing service dependencies.
        service_name (str): The name of the service to analyze.
        assoc_lst (List[str]): List of association names to filter dependencies.
        flag (bool): Flag indicating reverse or forward dependencies.

    Returns:
        None
    """
    if len(assoc_lst) == 0:
        key_list = ["grey66", "black"]
        print("No Assoc")
 
        for allowed_colour in key_list:
            print(allowed_colour)
 
        if flag:
            print("Reverse Deps")
            for service, depends in dependencies.items():
                if service_name in service:
                    for dep, colour in depends.items():
                        for allowed_colour in key_list:
                            if '[color="'+allowed_colour+'"];' in colour:
                                print(f" * {dep}")
        else:
            print("Forward Deps")
            for service, depends in dependencies.items():
                is_colour=False
                is_substring = any(service_name in s for s in depends)
                for dep, colour in depends.items():
                    for allowed_colour in key_list:
                        if '[color="'+allowed_colour+'"];' in colour and '"' + service_name + '"' == dep :
 
                            #print(f"dep = {dep}")
 
                            #print(allowed_colour)
                            #print(f" * {service}")
                            is_colour = True
                if is_substring and is_colour:
                    #print(f"depends = {depends}")
                    print(f" * {service} ")
 
    else:
        print("Assoc")
        print("ELSE")
        local_assoc_mapping = []
        print(assoc_lst)
        key_list = []
        for a_name in assoc_lst:
            for key in legends_dict.keys():
                if legends_dict[key].lower() == a_name.lower():
                    key_list.append(key)
 
        for allowed_colour in key_list:
            print(allowed_colour)
 
        if flag:
            print("Reverse Deps")
            for service, depends in dependencies.items():
                if service_name in service:
                    for dep, colour in depends.items():
                        for allowed_colour in key_list:
                            if '[color="'+allowed_colour+'"];' in colour:
                                print(f" * {dep}")
        else:
            print("Forward Deps")
            for service, depends in dependencies.items():
                is_colour=False
                is_substring = any(service_name in s for s in depends)
                for dep, colour in depends.items():
                    for allowed_colour in key_list:
                        if '[color="'+allowed_colour+'"];' in colour and '"' + service_name + '"' == dep :
 
                            #print(f"dep = {dep}")
 
                            #print(allowed_colour)
                            #print(f" * {service}")
                            is_colour = True
                if is_substring and is_colour:
                    #print(f"depends = {depends}")
                    print(f" * {service} ")


def print_dict(dic: Dict):
    """
    Print a dictionary.

    Args:
        dic (Dict): The dictionary to be printed.

    Returns:
        None
    """
    for k, v in dic.items():
        print(f'{k} -> {v}')
        print("---")


def dict_parser(file_path: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Parse a dot file and create a dictionary of service dependencies.

    Args:
        file_path (str): The path to the dot file.

    Returns:
        Dict[str, Dict[str, List[str]]]: The parsed dictionary.
    """
    main_dict = {}
    with open(file_path, "r") as dotfile:
        for line in dotfile:
            if "color" in line:
                key, value = line.strip().split("->")
                values_list = value.split()
                #print(f'{key} -> {values_list}')
                if key not in main_dict:
                    main_dict[key] = {}
 
                inner_dict = main_dict[key]
 
                for i in range(0, len(values_list) - 1):
                    if values_list[i] not in inner_dict:
                        inner_dict[values_list[i]] = []
                    inner_dict[values_list[i]].append(values_list[i + 1])
    #print_dict(main_dict)
    return main_dict


def create_temp(file_path: str) -> str:
    """
    Create a temporary dot file without ignored colors.

    Args:
        file_path (str): The path to the original dot file.

    Returns:
        str: The path to the temporary dot file.
    """
    filter_content = []
    with open(file_path, "r") as org_file:
        for line in org_file:
            if not any('color="' + exclusion_color in line for exclusion_color in ignore_color):
                filter_content.append(line)
 
 
    temp_file = "temp-" + file_path
    with open(temp_file, "w") as dest_file:
        dest_file.writelines(filter_content)
 
    return temp_file


def main():
    """
    Main function to parse command line arguments and execute the dependency analysis.
    """
    
    parser = argparse.ArgumentParser(description="Systemd Unit File Dependency Parser")
    parser.add_argument("-f", "--file", type=argparse.FileType('r'), help="pass the systemd-analyze's output dot file to be parsed", required=True)
    parser.add_argument("-r", "--reverse", action="store_true", help="pass to get the reverse dependency for the systemd unit file")
    parser.add_argument("-u", "--unit-files", nargs="+", help="pass one or more unit files to find dependencies", required=True)
    parser.add_argument("-a", "--association", nargs="+", help="pass one or more associations like Requires, Wants, After to find specific dependencies")
 
    args = parser.parse_args()
    file_path = args.file.name
 
    temp_file = create_temp(file_path)
    parsed_Dictionary = dict_parser(temp_file)
 
    reverse_Flag = 1
    if args.reverse:
        reverse_Flag = 0
    assoc_list = []
    if args.unit_files:
        if args.association:
            for assoc in args.association:
                assoc_list.append(assoc)
 
        for service_name in args.unit_files:
            print(f'\n|== Analyzing - [{service_name}]')
            depend_parser(parsed_Dictionary, service_name, assoc_list, reverse_Flag)


if __name__ == "__main__":
    main()
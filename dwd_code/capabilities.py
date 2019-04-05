import re


from dwd_code.dwd_ftp_connect import  FtpSearch


def main(stationId):
    """
    :param stationId: String
    :return: Dictionary
    """
    temporary1 = []
    temporary2 = []
    temporary3 = []
    temporary4 = []
    temporary5 = []

    all_files, _file_path = FtpSearch(resolution = None,observation_type = None, stationId=stationId)

    for file in all_files:

        path_name = re.split('climate/', file)[-1]

        if path_name.startswith('10_minutes'):

            path_split = path_name.split('/')
            temporary1.append(path_split[1])

        elif path_name.startswith('1_minute'):

            path_split = path_name.split('/')
            temporary2.append(path_split[1])

        elif path_name.startswith('daily'):
            path_split = path_name.split('/')
            temporary3.append(path_split[1])

        elif path_name.startswith('hourly'):
            path_split = path_name.split('/')
            temporary4.append(path_split[1])

        elif path_name.startswith('monthly'):
            path_split = path_name.split('/')
            temporary5.append(path_split[1])

    list_format1 = list(dict.fromkeys(temporary1)) # To remove the duplication in the dict.
    list_format2 = list(dict.fromkeys(temporary2))
    list_format3 = list(dict.fromkeys(temporary3))
    list_format4 = list(dict.fromkeys(temporary4))
    list_format5 = list(dict.fromkeys(temporary5))

    dicto = {
        "stationId": stationId,
        "capabilities": [
            {
                "resolution": "10_minutes",
                "observationTypes": list_format1
            },
            {
                "resolution": "1_minute",
                "observationTypes": list_format2

            },
            {
                "resolution": "daily",
                "observationTypes": list_format3
            },
            {
                "resolution": "hourly",
                "observationTypes": list_format4
            },
            {
                "resolution": "monthly",
                "observationTypes": list_format5
            }
        ]
    }

    return (dicto)

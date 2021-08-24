import os
import easygui
import pandas as pd


def open_directory():
    input_file = easygui.diropenbox(msg="Choose a directory with 'Automatic Fiber Tracking' data",
                                    default=r"/home/lg/Science/dti/")
    return input_file


def read_directories(root_directory: str) -> list:
    file_list = []
    for path, folder, files in os.walk(root_directory):
        for file in files:
            if file.endswith('stat.txt'):
                file_list.append([path, file])
    return file_list


def parse_stat_file(file_list):
    anat_list = []
    subj_list = []
    param_list = ['iso', 'qa', 'dti_fa']

    for stat_file in file_list:
        with open(f"{stat_file[0]}/{stat_file[1]}", 'r') as file:
            sentence = file.read().split('\n')
            subj_list.append(sub_name_parser(stat_file[1]))
            for sent in range(len(sentence)):
                anat_list.append(area_name_parser(stat_file[1]))
    dict_coeff = {
        i:
            {
                f"{anat}____{subj}": 0 for anat in set(anat_list) for subj in set(subj_list)
            }
        for i in set(param_list)
    }

    for stat_file in file_list:
        try:
            with open(f"{stat_file[0]}/{stat_file[1]}", 'r') as file:
                sentence = file.read().split('\n')
                subj_list.append(sub_name_parser(stat_file[1]))
                for sent in range(len(sentence)):
                    if sentence[sent].split('\t')[0] in param_list:
                        dict_coeff[sentence[sent].split('\t')[0]].update(
                            {
                                f"{area_name_parser(stat_file[1])}____{sub_name_parser(stat_file[1])}":
                                    sentence[sent].split('\t')[1]
                            }
                        )
        except FileExistsError:
            print(f"file {stat_file[0]}/{stat_file[1]} not found")
        except IndexError:
            print(f"list index out of range in {stat_file[0]}/{stat_file[1]}")
    return dict_coeff


def sub_name_parser(word: str) -> str:
    word_ = word.split('.')
    name = word_[0].split('_')
    return name[2].rstrip('.')


def area_name_parser(word: str) -> str:
    name = word.split('.')
    return name[1]


def generate_year_document(dict_: dict, directory: str) -> None:
    df = pd.DataFrame(dict_)
    df.to_excel(f"{directory}/dsi_report.xlsx")


if __name__ == '__main__':
    DIRECTORY = open_directory()
    generate_year_document(parse_stat_file(read_directories(DIRECTORY)), DIRECTORY)
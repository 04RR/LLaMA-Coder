from big_projects.utils import *
import os
import json


def get_test_file_path(program_file_path):
    path_parts = os.path.split(program_file_path)
    test_dir = path_parts[0].replace("files", "tests")
    test_file_name = (
        os.path.splitext(path_parts[1])[0]
        + "_test"
        + os.path.splitext(path_parts[1])[1]
    )
    test_file_path = os.path.join(test_dir, test_file_name)

    return test_file_path


class CodeFile:
    def __init__(self, code_string, path, base_path):
        self.content = ""
        self.code_string = code_string
        self.test_code_string = """"""
        self.path = base_path + path
        self.tested = False
        self.test_result = False
        self.test_file_path = get_test_file_path(path)
        self.test_code_string = ""
        self.base_path = base_path

    def write(self, code_string=None, path=None):
        if code_string is None:
            code_string = self.code_string
        if path is None:
            path = self.path
            
        try:
            with open(path, "w") as file:
                file.write(code_string)

        except:
            folder_name = self.base_path + path.replace(self.base_path, "\\").split("/")[0]
            os.mkdir(folder_name)
            with open(self.base_path + path.replace(self.base_path, "\\").replace("/", "\\"), "w") as file:
                file.write(code_string)

    def test(self, test_code_string=None):
        if test_code_string is None:
            test_code_string = self.test_code_string

        self.write(test_code_string, self.test_file_path)
        self.test_result, self.tested = run_code(test_code_string, save=False)

        return self.test_result, self.tested

    def __repr__(self):
        return f"CodeFile({self.path})"

    def __str__(self):
        return f"CodeFile({self.path})"


def main(task, base_path):

    model = "4"  # "3.5-turbo" or "4"

    files_prompt = f"""Task: {task}\n
    What all code files are needed to complete this task?\n
    eg: eg: utils.py, dataset.py, models.py, trainer.py and other such files are needed to perform a task that involves training a model on a given dataset.\n
    Give the names of all the files along with the file extensions that are needed to complete this task, make everything lowercase and use underscores instead of spaces. Keep in mind to make the project modular and readable and seperate code in different files based on their functionality.\n
    Seperate the names of the files with commas. Only give filenames and nothing else no explainations or anything else. If a folder has to be made list the files in the folder as folder_name/file_name.py. Give only the names of the files and nothing else."""
    code_files = get_code(files_prompt).split(", ")
    if code_files[-1].endswith("."):
        code_files[-1] = code_files[-1][:-1]
    code_files.sort(reverse=True)
    print("Code files:", code_files)

    prompt = f"""Task: {task}\nfiles: {code_files}
        Write a detailed summary of what each file does and list all variables, functions and class each file should contain. also include the function/class definition in each file along with what it returns if any. your response should be in the form of a json where the key is the name of the file and the value is a multiline string of the summary of the file. Give only the json with no other text."""

    response = get_response_1(prompt, model=model)
    with open(f"codes\project_2\summary.json", "w") as file:
        file.write(response)

    summary_dict = {}
    with open(f"codes\project_2\summary.json", "r") as file:
        summary_dict = json.load(file)

    code_files = [CodeFile("", code_file, base_path) for code_file in code_files]
    code_prompt = f""""Task: {task}\nfiles: {code_files}\nOther Files in the repo- RAJESH\nFile summary- \nRAKSHITH\nWrite code in python ROHIT, make the code modular and follow the best practices of python. Use OOP methods. Write only the code needed for this particular file (ROHIT).\nGive only the code for this file and nothing else.\nimport all the necessary packages required"""

    for code_file in code_files:
        other_summery = ""
        for key in summary_dict.keys():
            if key != code_file.path.split("\\")[-1]:
                other_summery += summary_dict[key] + "\n"
        code_summary = summary_dict[code_file.path.split("\\")[-1]]
        code_file.code_string = get_code(
            code_prompt.replace("ROHIT", code_file.path)
            .replace("RAKSHITH", code_summary)
            .replace("RAJESH", other_summery),
            model=model,
        )
        code_file.write()

        # test_prompt = f"""Task: {task}\n files: {code_files}\n Code -\n{code_file.code_string}\nWrite python code to perform tests on code given above. Make sure to test all the funtions and classes in the code. Make the tests robust. Give only the code and nothing else."""
        # test_code_string = get_code(test_prompt, model="4")
        # test_prompt = f"""Code= \n{test_code_string}\nDoes this code have any errors? If it does return the full code without the error and if there are no errors give me the entire code back. Don't give any other text in the response other than code. import all the necessary packages"""
        # code_file.test_code_string = get_code(test_prompt, model=model)
        # code_file.write(test_code_string, code_file.test_file_path)

        # while code_file.tested == False:
        #     code_file.test()
        #     test_prompt = f"""Code= \n{code_file.test_code_string}\nDoes this code have any errors? If it does return the full code without the error and if there are no errors give me the entire code back. Don't give any other text in the response other than code."""
        #     code_file.test_code_string = get_code(test_prompt)


if __name__ == "__main__":
    base_path = r"D:\Desktop\Shree\codes\project_2\files\\"
    main(
        "Make a landing page for a fintech startup called goalZ. Add a nav bar with the company name and 'About' and 'Contact'. Add a Signup to waitlist where users can login with their google accounts and their name and email is saved in a sqllite database.",
        base_path,
    )


# complete the code_file filling part with running test code and checking for errors
# find which one is the main file and run it
# look for errors, if there are any, look for which file to fix. Propmt the model with the error and the code that gave error and fix it.

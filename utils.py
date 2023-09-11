import subprocess
import os
import pandas as pd
import io


def run_code(code_string, code_dir=r"./"):
    path = os.path.join(code_dir, "temp_script.py")
    with open(path, "w") as file:
        file.write(code_string)

    

def df_info(df):
    pd.options.display.max_colwidth = 500
    pd.options.display.expand_frame_repr = False

    with io.StringIO() as buffer:
        df.info(buf=buffer)
        info_output = buffer.getvalue()

    return f"""df info -\n{info_output}\n\ndf.head -\n{df.head()}\n\ndf.describe -\n{df.describe()}\n\ndf.columns -{list(df.columns)}"""

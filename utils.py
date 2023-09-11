import openai
import subprocess
import os

openai.organization = "org-E6WUWsDXimggLNGM1saEKRwh"
openai.api_key = "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"


def run_code(code_string, save=True, code_dir=r"D:\Desktop\CoderGPT\gptcodes"):
    path = os.path.join(code_dir, "temp_script.py")
    with open(path, "w") as file:
        file.write(code_string)

    result = subprocess.run(
        ["python", f"{code_dir}/temp_script.py"], capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return (result.stderr, False)
    else:
        return (result.stdout, True)


def get_code(prompt, model= "3.5-turbo"):
    response = (
        openai.ChatCompletion.create(
            model=f"gpt-{model}",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )["choices"][0]["message"]["content"]
    )
    try:
        response = response.split("```")[1].replace("python", "").replace("html", "").replace("css", "").strip()
    except:
        pass
    
    return response


def get_response(prompt, model= "3.5-turbo"):
    response = (
        openai.ChatCompletion.create(
            model=f"gpt-{model}",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )["choices"][0]["message"]["content"]
    )
    
    return response


def get_response_1(prompt, model= "3.5-turbo"):
    response = (
        openai.ChatCompletion.create(
            model=f"gpt-{model}",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )["choices"][0]["message"]["content"]
    )

    prompt = prompt + response + "\nis your response complete? respond with only yes if it is complete. if it is not reply with only the rest of the response to complete your response and continue where you left off."

    response_1 = (
        openai.ChatCompletion.create(
            model=f"gpt-{model}",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )["choices"][0]["message"]["content"] 
    )
    if response_1.lower() == "yes":
        return response
    else:
        return response + response_1
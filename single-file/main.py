from typing import List, Union
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import streamlit as st
from langchain.llms.fake import FakeListLLM
from utils import df_info


df = pd.DataFrame()
csv_path = "" # change file path
sys_msg = f"""You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

def init_page():
    st.set_page_config(page_title="subpixel", page_icon=":robot_face:")
    st.header("subpixel")
    st.sidebar.title("")


def init_messages():
    # st.sidebar.markdown("### Upload CSV")
    # csv_file = st.sidebar.file_uploader(
    #     "Upload CSV file with messages", type=["csv"], key="csv"
    # )
    df_information = ""

    try:
        df = pd.read_csv(csv_path)
        df_information = df_info(df)

        sys_msg = f"You are a helpful Coding AI assistant. Reply your answer in mardkown format. You have access to a pandas dataframe named `df` that has the following information:\n\n{df_information}\n\nCode the necessary things based on the information provided above.\nthe csv file is in {csv_path}"
        
        with open("sys_msg.txt", "w") as file:
            file.write(sys_msg)

        clear_button = st.sidebar.button("Clear Conversation", key="clear")

        if clear_button or "messages" not in st.session_state:
            st.session_state.messages = [SystemMessage(content=sys_msg)]
    except:
        pass


def get_llm(model_path):
    temperature = 0.9
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    return LlamaCpp(
        model_path=f"{model_path}",
        input={"temperature": temperature, "max_length": 2000, "top_p": 1},
        callback_manager=callback_manager,
        verbose=False,
    )


def get_answer(llm, messages):
    return llm(llama_v2_prompt(convert_langchainschema_to_dict(messages)))


def find_role(message: Union[SystemMessage, HumanMessage, AIMessage]):
    """
    Identify role name from langchain.schema object.
    """
    if isinstance(message, SystemMessage):
        return "system"
    if isinstance(message, HumanMessage):
        return "user"
    if isinstance(message, AIMessage):
        return "assistant"
    raise TypeError("Unknown message type.")


def convert_langchainschema_to_dict(
    messages: List[Union[SystemMessage, HumanMessage, AIMessage]]
):
    return [
        {"role": find_role(message), "content": message.content} for message in messages
    ]


def llama_v2_prompt(messages: List[dict]):
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    BOS, EOS = "<s>", "</s>"
    DEFAULT_SYSTEM_PROMPT = sys_msg

    if messages[0]["role"] != "system":
        messages = [
            {
                "role": "system",
                "content": DEFAULT_SYSTEM_PROMPT,
            }
        ] + messages
    messages = [
        {
            "role": messages[1]["role"],
            "content": B_SYS + messages[0]["content"] + E_SYS + messages[1]["content"],
        }
    ] + messages[2:]

    messages_list = [
        f"{BOS}{B_INST} {(prompt['content']).strip()} {E_INST} {(answer['content']).strip()} {EOS}"
        for prompt, answer in zip(messages[::2], messages[1::2])
    ]
    messages_list.append(f"{BOS}{B_INST} {(messages[-1]['content']).strip()} {E_INST}")

    return "".join(messages_list)


def main():
    _ = load_dotenv(find_dotenv())

    init_page()
    # llm = get_llm(model_path)
    responses = ["Action: Python REPL\nAction Input: print(2 + 2)", "Final Answer: 4"]
    llm = FakeListLLM(responses=responses)
    init_messages()

    if user_input := st.chat_input("Explore your data!"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Analysing Data..."):
            answer = get_answer(llm, st.session_state.messages)
            # answer = user_input

        st.session_state.messages.append(AIMessage(content=answer))

    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)


if __name__ == "__main__":
    main()

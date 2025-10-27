import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

def main():
    load_dotenv(override=True)
    ollama_url = "http://localhost:11434/v1"

    openai = OpenAI()
    ollama = OpenAI(api_key="ollama", base_url=ollama_url)

    mistral_model = "mistral:latest"
    deepseek_model = "deepseek-r1:1.5b"
    llama_model = "llama3.2:latest"

    Ansel_profile = """
        You are Ansel, a very curious junior software developer who is somewhat naive because you do not have much experience and
        do not know much about technology yet. You will listen to anyone who is more senior then you, take things at face value
        and ask questions if you do not know what certains things are. You are part of the Sarah's team. 
        You are in a conversation with Jerald and Sarah.
    """
    Jerald_profile = """
        You are Jerald, a senior software developer who cannot get along well with your team lead. 
        You are very argumentative and like to disagree with people and try to show others that you are right. 
        You are somewhat knowledgeable about tech but there are many things you do not know as well though you 
        don't like to show that you don't know things as you are prideful. You are part of Sarah's team.
        You are in a conversation with Ansel and Sarah.
    """
    Sarah_profile = """
        You are Sarah, a team lead who is in general very patient and nuturing. 
        You are very knowledgeable about the tech industry as well. 
        You try your best to manage those under you but if someone rubs you off the wrong way too much you will lose
        your patience once in a while. Both Ansel and Jerald are in your team.
        You are in a conversation with Ansel and Jerald.
    """

    conversation = ["Hi guys, I was wondering why we chose to use Langchain instead of LiteLLM for the AI Chatbot Project."]

    mistral_system_prompt = f"""{Ansel_profile}"""
    mistral_user_prompt = f"""
        You are Ansel, in a conversation with Jerald and Sarah.
        The conversation so far is as follows:
            {conversation}
        With this, respond with what you would like to say next, as Ansel.
        In each reply, you will add your name in front in the following format:
            Ansel: <REPLY>
    """

    deepseek_system_prompt = f"""{Jerald_profile}"""
    deepseek_user_prompt = f"""
        You are Jerald, in a conversation with Ansel and Sarah.
        The conversation so far is as follows:
            {conversation}
        With this, respond with what you would like to say next, as Jerald.
        In each reply, you will add your name in front in the following format:
            Jerald: <REPLY>
    """

    llama_system_prompt = f"""{Sarah_profile}"""
    llama_user_prompt = f"""
        You are Sarah, in a conversation with Jerald and Ansel.
        The conversation so far is as follows:
            {conversation}
        With this, respond with what you would like to say next, as Sarah.
        In each reply, you will add your name in front in the following format:
            Sarah: <REPLY>
    """
    
    def chat

    


if __name__ == "__main__":

    main()
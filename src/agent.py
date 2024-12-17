from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
from src.utils import set_api_key_env, get_text_from_file
from dotenv import load_dotenv
import os


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
set_api_key_env("OPENAI_API_KEY", openai_api_key)

llm = ChatOpenAI(model="gpt-4o")

prompt = get_text_from_file("prompt.md")

information =  "Details: "
prompt_template = ChatPromptTemplate([
    ("system", prompt),
    ("user", "Write an email with provided instructions and to the following people:{information}"),
])


email_agent = prompt_template | llm


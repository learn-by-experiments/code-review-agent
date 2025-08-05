import dotenv
from langchain_ollama.chat_models import ChatOllama

dotenv.load_dotenv()

# from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
# from gen_ai_hub.proxy.langchain.openai import ChatOpenAI

# proxy_client = get_proxy_client("gen-ai-hub")
# # non-chat model
# model_name = "gpt-4o-mini"

# llm = ChatOpenAI(proxy_model_name=model_name, proxy_client=proxy_client)


ollama_model_name = "llama3.1"

llm = ChatOllama(model=ollama_model_name)

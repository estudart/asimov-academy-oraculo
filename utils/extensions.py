from langchain_openai import ChatOpenAI

# from src.adapters.logger_adapter import LoggerAdapter
# from sqlalchemy.ext.declarative import declarative_base
from adapters.secrets_adapter import SecretsAdapter



secrets_adapter = SecretsAdapter()
# fix this later on
# model = ChatOpenAI(api_key=secrets_adapter.get_secret().get("OPENAI_API_KEY"))
# Base = declarative_base()
# logger = LoggerAdapter().get_logger()

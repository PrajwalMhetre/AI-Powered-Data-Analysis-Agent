from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from core.config import settings
from utils.logger import get_logger

logger = get_logger("data_agent")

def get_llm():
    """Factory to get the correct LLM based on environment variables for security/privacy choices"""
    provider = settings.LLM_PROVIDER
    if provider == "openai":
        return ChatOpenAI(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_MODEL, temperature=0)
    elif provider == "anthropic":
        return ChatAnthropic(api_key=settings.ANTHROPIC_API_KEY, model_name=settings.ANTHROPIC_MODEL, temperature=0)
    elif provider == "ollama":
        # Zero-leak Local Execution
        return ChatOllama(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL, temperature=0)
    else:
        raise ValueError(f"Unknown LLM Provider: {provider}")

def analyze_dataframe(df: pd.DataFrame, query: str) -> str:
    """
    Takes a pandas DataFrame and a natural language query.
    Generates python code, executes it (self-correcting on error), and returns the insight.
    """
    try:
        llm = get_llm()
        
        # create_pandas_dataframe_agent runs the LLM in a loop where it generates python code,
        # executes it via an AST sandbox evaluation or python REPL, and self-corrects on Error.
        agent = create_pandas_dataframe_agent(
            llm, 
            df, 
            verbose=True, 
            agent_type="openai-tools" if settings.LLM_PROVIDER == "openai" else "zero-shot-react-description",
            allow_dangerous_code=True, # Explicitly allowing under docker isolation context.
            handle_parsing_errors=True # Auto self-correct
        )
        
        logger.info(f"Executing query on Dataframe: {query}")
        result = agent.invoke({"input": query})
        
        return result.get("output", str(result))
    except Exception as e:
        logger.error(f"Agent analysis failed: {str(e)}")
        raise e

def generate_executive_summary(df: pd.DataFrame) -> str:
    """Autonomous Insights Generator"""
    llm = get_llm()
    prompt = f"""
    You are a Senior Data Analyst. I will provide you with a summary of a dataset (describe and info).
    You need to write a 3 paragraph Executive Summary highlighting obvious trends, statistical anomalies, 
    and actionable business advice.
    
    Columns: {', '.join(df.columns.tolist())}
    Shape: {df.shape}
    Describe: {df.describe().to_string()}
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        logger.error(f"Executive Summary failed: {str(e)}")
        raise e

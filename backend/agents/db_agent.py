from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
from core.config import settings
from agents.data_agent import get_llm
from utils.logger import get_logger

logger = get_logger("db_agent")

def analyze_sql_database(db_uri: str, query: str) -> str:
    """
    Connects to Postgres, MongoDB (via BI connector SQL), or Snowflake.
    Executes natural language queries.
    """
    try:
        # Connect to DB (Read-Only context should be enforced in the URI string by client)
        db = SQLDatabase.from_uri(db_uri)
        llm = get_llm()
        
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=None, 
            db=db,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
        
        logger.info(f"Executing SQL Agent on DB with query: {query}")
        result = agent_executor.invoke({"input": query})
        
        return result.get("output", str(result))
    except Exception as e:
        logger.error(f"DB Agent analysis failed: {str(e)}")
        raise e

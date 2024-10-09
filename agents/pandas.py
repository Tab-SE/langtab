import os, re, json, logging, pandas as pd

from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from modules import headless

# Set up the logger
logger = logging.getLogger(__name__)

def analyze(query):
    try:
        payload = get_payload(query)
        vds_data = headless.query(payload)
        # Create a pandas DataFrame from the JSON data
        df = pd.DataFrame(vds_data)

        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model=os.environ['PANDAS_AGENT_MODEL']),
            df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            allow_dangerous_code=True,
        )

        instruct_header = "Answer the following query directly by executing the necessary python code. Give a succinct explanation of the steps you took and how you know the answer is correct: "

        operation = agent.invoke(instruct_header + query)

        input = operation['input']
        output = operation['output']

        logger.info(f"***** PANDAS AGENT Input *****\nType: {type(input)}\nInput: {input}")
        logger.info('-----------------------------------------')
        logger.info(f"***** PANDAS AGENT Output *****\nType: {type(output)}\nOutput: {output}")

        return output
    except KeyError as e:
        # Log the error
        logger.error(f"KeyError occurred: {e}")
    except Exception as e:
        # Log any other errors
        logger.error(f"An error occurred during analysis: {e}")


def get_payload(output):
    # output reasoning
    logger.info(output.split('JSON_payload')[0])
    # parse LLM output and query headless BI
    parsed_output = output.split('JSON_payload')[1]

    match = re.search(r'{.*}', parsed_output, re.DOTALL)
    if match:
        json_string = match.group(0)
        payload = json.loads(json_string)
        return payload

import argparse, uvicorn, asyncio
from dotenv import load_dotenv
from modules import chain_config, serve, logging_config
import logging

# Get the logger
logger = logging.getLogger(__name__)

# runs interactively in the terminal
def run_interactive_mode(chain):
    active_utterance = get_utterance()
    while active_utterance.lower() != 'stop':
        # Log the user input
        logger.info(f"User input: {active_utterance}")

        try:
            # Invoke the chain with the user input and capture the response
            response = chain.invoke(active_utterance)

            # Log the response from the LLM
            logger.info(f"LLM Response: {response}")

            # Print the response to the user
            print(response)

        except Exception as e:
            # Log any error that occurs during the invocation
            logger.error(f"Error while processing input '{active_utterance}': {e}")

        # Prompt the user for the next input
        active_utterance = get_utterance()

# runs as a service via Langserve
def run_api_mode(chain, host, port=8000):
    app = serve.langtab_agent(chain)
    logger.info(f"Starting API mode on {host}:{port}...")
    uvicorn.run(app, host=host, port=port)

# prompts the user to continue asking questions
def get_utterance():
    query = input('What would you like to know about your data? Reply with "stop" if you are done.\n')
    return query

def main():
    # Start logger
    logger.info("Starting the main function...")

    # Load environment variables
    load_dotenv()

    # Parse arguments for running the application in different modes
    parser = argparse.ArgumentParser(description="Run the NLQ2VDS agent in interactive or API mode.")
    parser.add_argument("--mode", choices=["interactive", "api"], default="interactive", help="Run mode: interactive or api")
    parser.add_argument("--host", default="localhost", help="Host for API mode")
    parser.add_argument("--port", type=int, default=8000, help="Port for API mode")
    args = parser.parse_args()

    # Create the chain configuration
    chain = chain_config.create_chain()

    # Run in either interactive or API mode based on the arguments
    if args.mode == "interactive":
        run_interactive_mode(chain)
    else:
        run_api_mode(chain, args.host, args.port)

if __name__ == "__main__":
    main()

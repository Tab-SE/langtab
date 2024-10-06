from fastapi import FastAPI
from langserve import add_routes

from modules.server import serialize


def langtab_agent(chain):
    # define the server app
    app = FastAPI(
    title="Tableau Headless BI Query Chain",
    version="1.0",
    description="An early demonstration of a LangChain chain querying Tableau's Headless BI service",
    )

    # configures chain to use the custom serializer
    serialized_chain = chain.with_config(serializer=serialize.CustomSerializer())

    # use Langserve to serve up the agent
    add_routes(
        app,
        serialized_chain,
        path="/headlessbi",
    )

    return app

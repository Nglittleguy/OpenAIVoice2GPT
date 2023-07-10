from langchain.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities import ApifyWrapper
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)
os.environ.get("OPEN_API_KEY")
os.environ.get("APIFY_API_TOKEN")

apify = ApifyWrapper()

loader = apify.call_actor(
    actor_id="apify/website-content-crawler",
    run_input={"startUrls": [{"url": "https://en.wikipedia.org/wiki/Threads_(social_network)"}]},
    dataset_mapping_function=lambda item: Document(
        page_content=item["text"] or "", metadata={"source": item["url"]}
    ),
)

index = VectorstoreIndexCreator().from_loaders([loader])
query = "What is the internal name of Threads?"
result = index.query_with_sources(query)

print(result["answer"])
print(result["sources"])
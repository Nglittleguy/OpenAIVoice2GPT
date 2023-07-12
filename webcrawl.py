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
    run_input={"startUrls": [{"url": "https://www.marriott.com/default.mi"}]},
    dataset_mapping_function=lambda item: Document(
        page_content=item["text"] or "", metadata={"source": item["url"]}
    ),
)

index = VectorstoreIndexCreator().from_loaders([loader])
query = "What parameters do I need to book a room?"
result = index.query_with_sources(query)

print(result["answer"])
print(result["sources"])
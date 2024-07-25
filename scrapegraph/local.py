from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

graph_config = {
   "llm": {
      "model": "ollama/mistral",
      "temperature": 1,
      "format": "json",  # Ollama needs the format to be specified explicitly
      #"model_tokens": 2000, #  depending on the model set context length
      "base_url": "http://localhost:11434",  # set ollama URL of the local host (YOU CAN CHANGE IT, if you have a different endpoint
   },
   "embeddings": {
      "model": "ollama/nomic-embed-text",
      "temperature": 0,
      "base_url": "http://localhost:11434",  # set ollama URL
   }
}

# ************************************************
# Create the SmartScraperGraph instance and run it
# ************************************************

smart_scraper_graph = SmartScraperGraph(
   prompt="List me company description, who we are, who are you, company reviews, bond description.",
   # also accepts a string with the already downloaded HTML code
   source="https://mgsuretybonds.com/",
   config=graph_config
)

result = smart_scraper_graph.run()
print(result)
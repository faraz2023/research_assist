# research_assist
Tool that uses tavily and langraph to conduct research, then gsuite apis to organize it

## Example usage 

The main imports. If running in a notebook you can also display the 
reports in markdown
```commandline
from research_assist.researcher.Agent import ResearchAgent, load_secrets
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from research_assist.gsuite.drive.GoogleDriveHelper import GoogleDriveHelper
from research_assist.gsuite.docs.GoogleDocsHelper import GoogleDocsHelper
from IPython.display import Markdown
```

Set up a Google cloud service account and give it read/write permissions to one of 
your drive folders. This example folder is called AIAssistant
```commandline
drive_helper = GoogleDriveHelper(folder_name="AIAssistant")
```

Set up a folder structure to write reports
```commandline
test_folder = drive_helper.create_new_folder("research_projects_nov_2024")
```

Set up models to be used in the agent
```commandline
secrets = load_secrets()
model = ChatOpenAI(
    model="gpt-4o-mini", temperature=0, api_key=secrets["OPENAI_API_KEY"]
)
tavily = TavilyClient(api_key=secrets["TAVILY_API_KEY"])
agent = ResearchAgent(model, tavily)
```
Run the report generation
```commandline
task = "What are the key trends in LLM reseach and application that you see in 2024"
result = agent.run_task(task_description=task,max_revisions=3)
```

You can access the outputs in the result list, or using the agent memory
```commandline
agent.in_memory_store.search(("1", "memories"))
```

To write some text to a Google doc
```commandline
text_to_insert = result[6]["write"]["draft"]
docs_helper = GoogleDocsHelper()
test_document_id = drive_helper.create_basic_document("LLM_2024",parent_folder_id=test_folder)
idx = docs_helper.create_doc_template_header("LLM trends",test_document_id)
idx = docs_helper.write_text_to_doc(start_index=idx,text=text_to_insert,doc_id=test_document_id)
```
# llama-parse is async-first, running the sync code in a notebook requires the use of nest_asyncio
import nest_asyncio
from llama_parse import LlamaParse
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
import json
nest_asyncio.apply()

import os

os.environ["LLAMA_CLOUD_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""

embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-3.5-turbo-0125")

Settings.llm = llm

text = ""

documents =  LlamaParse(result_type="markdown",verbose=True)
json_objs = documents.get_json_result("doc/65D-30_Redacted.pdf")
json_list = json_objs[0]["pages"]
# print(json_list)
json_list = json_objs[0]["pages"]
for page in json_list:
    # print(page["text"])
    text += page["text"]
    # print(text)
# print(json_objs[0]["pages"].json())
# for page in json_list:
#     # text += page["text"]
#     # print(page.json())
#     # print("end")
#     json_string = json.dumps(page)
#     print(json_string[0])
#     break
# print("=-"*20, text)
with open('gathered.txt', 'w') as file:
    file.write(text)

print(text)
regs = [line for line in text.splitlines() if line.startswith("65D")]
print(regs, "111111111111111")
# with open('gathered_text.txt', 'w') as file:
#     file.write(str(regs))

# print("Text has been written to gathered_text.txt")

# with open("gathered.txt", "r") as file:
#     data = file.read()
# print(data)
# filtered_data = [line for line in data.splitlines() if line.startswith("65D")]
# print(filtered_data)
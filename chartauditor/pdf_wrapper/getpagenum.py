import nest_asyncio
from llama_parse import LlamaParse
from llama_index.core.schema import BaseNode, TextNode, Document
import os

os.environ["LLAMA_CLOUD_API_KEY"] = "llx-yy6f3PverY6TamVVnPJ8rr2lAG9k6G3hSemwjUClGexQsfRy"
# def extracting_content(pdf_path):
#     documents = LlamaParse(result_type="markdown", parsing_instruction="write the page number by order(from 1 page to 8 page) extracting the pdf ").load_data(pdf_path)
#     # text = documents[0].text
    
#     # print(documents)
#     return documents

path = "doc/split_aveatester.pdf"
parser = LlamaParse(verbose=True)
json_objs = parser.get_json_result(path)
json_list = json_objs[0]["pages"]

documents = []
All_Text = ""

for _, page in enumerate(json_list):
    documents.append(
        Document(
            text=page.get("text"),
            metadata=page,
        )
    )

for doc in documents:
    page =  doc.metadata
    pageNum = page["page"]
    All_Text += page["md"] + f"This is {pageNum} page."
    print("-=-=-=-=-=-=-=-=-=-=-=-=")



print(All_Text)
    # print(doc.id_, "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", doc.text.strip()[:10], "-=-=-=--------------------------------", doc.metadata)
    
# result = extracting_content(path)

# print(result)


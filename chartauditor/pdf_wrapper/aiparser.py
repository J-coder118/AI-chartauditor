import pytesseract
from PIL import Image
import pdf2image
from PyPDF2 import PdfReader, PdfWriter
import nest_asyncio
from llama_parse import LlamaParse
from llama_index.core.schema import BaseNode, TextNode, Document
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import re
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["PATH"] += os.pathsep + r"C:\poppler\poppler-24.02.0\Library\bin"
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Tesseract-OCR"

os.environ["LLAMA_CLOUD_API_KEY"] = ""
ANTHROPIC_API_KEY = ""


import voyageai
from langchain_anthropic import ChatAnthropic

vo = voyageai.Client(api_key = "")

samReport = """# 65D-30 Audit Report  
 You are an expert auditor specializing in Substance Abuse, Substance Use, and Mental Health regulations in Florida. Your task is to evaluate a patient chart's compliance with specific regulations from 65D-30.

For each question asked about a specific 65D-30 regulation (e.g., "Based on the 65D-30.[specific regulation number]), provide a structured response using the following format:

## Regulatory Adherence to 65D-30.[specific regulation number]

- Examine the patient chart for compliance with 65D-30.[specific regulation number].
- Identify any discrepancies, lapses, or deviations from this regulation. Provide specific instances from the chart where these occur, referencing page numbers when possible.
- Offer detailed advice on how to address these issues to ensure the chart meets the requirements of this regulation.

## Recommendations
What they need to do to correct it to meet 65D-30.[specific regulation number]
## Score

- Assign a numeric score between 0-100 for the chart's compliance with 65D-30.[specific regulation number], where 0 indicates complete non-compliance and 100 indicates perfect compliance.

Please provide your response in nicely formatted markdown, with a minimum of 500 characters. If you are unsure about any findings, do not make anything up; simply provide factual output based on the information available in the provided documents.

Your responses will eventually be compiled into a larger report evaluating the patient chart's overall compliance with relevant 65D-30 regulations. Focus on providing a thorough, regulation-specific evaluation for each question asked.
  """

report = """
## Regulatory Adherence to 65D-30.0043 Placement  
- Review of the patient chart reveals the following issues with 65D-30.0043 Placement standards:  
  - No documentation of criteria and procedures for admitting, retaining, transferring and discharging individuals.    
  - No indication that the individual was assessed prior to admission to determine level of service need and choice.  
  - No referral to a proper level of care when the assessed level was not available.  
  - A primary counselor is not assigned to the individual.  
  - Orientation does not cover all required components (description of services, rights, admission/discharge policies, fees, rules, grievance process, confidentiality, advance directives).  
  - No physician documentation that individual is not being retained in a service beyond the provider's capability to meet their needs.  
  - Discharge/transfer summary with required elements is missing.  
  
- To rectify these problems and comply with 65D-30.0043, the provider should:  
  - Develop written criteria and procedures for admissions, retention, transfer and discharge.   
  - Ensure individuals are assessed pre-admission for appropriate level of care and referred out if that level is not available.    
  - Assign a primary counselor to each individual and document this in their chart.  
  - Provide a comprehensive orientation and document this, including all required topics per 65D-30.0043.  
  - Involve the physician in determinations and documentation around ability to meet individual's service needs.   
  - Provide individuals with a discharge/transfer summary that contains all elements required by 65D-30.0043.  
  - Implement a quality assurance process to audit records for these placement standards.  
  
### Score  
Based on the lack of evidence of compliance with most placement standards, this patient chart earns a 30 out of 100 for meeting 65D-30.0043 requirements.  
"""
batch_size = 70
def parse_pdf_with_ocr(pdf_path):
    # Convert PDF to images
    images = pdf2image.convert_from_path(pdf_path)

    parsed_text = ""
    for image in images:
        # Convert image to grayscale
        image = image.convert("L")

        # Perform OCR on the image
        text = pytesseract.image_to_string(image)
        parsed_text += text

    return parsed_text

def should_use_ocr(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)

        # Check if the PDF contains selectable text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            # print(text)
            if re.search(r'[♥$&]', str(text)) != None:
                print(pdf_path, "OCR parser")
                text = parse_pdf_with_ocr(pdf_path)
                print(len(text))
                with open('chart_OCR.txt', 'w') as file:
                    file.write(str(text))
                return True
            else:
                # Read the original PDF
                input_pdf = PdfReader(pdf_path)

                batch_size = 70
                num_batches = len(input_pdf.pages) // batch_size + 1
                text_content = ""
                # Extract batches of 100 pages from the PDF
                for b in range(num_batches):
                    # writer = PdfWriter()

                    # # Get the start and end page numbers for this batch
                    # start_page = b * batch_size
                    # end_page = min((b+1) * batch_size, len(input_pdf.pages))

                    # # Add pages in this batch to the writer
                    # for i in range(start_page, end_page):
                    #     writer.add_page(input_pdf.pages[i])

                    # Save the batch to a separate PDF file
                    batch_filename = f'split/output/{pdf_path}-batch{b+1}.pdf'
                    # with open(batch_filename, 'wb') as output_file:
                    #     writer.write(output_file)

                    # Now you can use the `partition_pdf` function from Unstructured.io to analyze the batch
                    text_content += extracting_content(batch_filename)

                data_list = convert_text_to_list(text_content)

                return data_list
        # # Check if the PDF contains scanned images or non-selectable content
        # for page_num in range(len(pdf_reader.pages)):
        #     page = pdf_reader.pages[page_num]
        #     if '/XObject' in page['/Resources'] and '/Image' in page['/Resources']['/XObject']:
        #         return True

    

# print(should_use_ocr("doc/split_RealChart.pdf"))


# print("llamaparse")


def extracting_content(pdf_path):
    # documents = LlamaParse(result_type="markdown").load_data(pdf_path)
    # text = documents[0].
    print(pdf_path)
    parser = LlamaParse(verbose=True)
    json_obj = parser.get_json_result(pdf_path)
    json_list = json_obj[0]["pages"]

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
        All_Text += page["md"] + f"This is real {pageNum} page."
    
    # print(len(text))
    return All_Text

def convert_text_to_list(text):
    keyword = "## "

    data_list = text.split(keyword)[1:]

    pdf_data_list = [keyword + data.strip() for data in data_list]
    return pdf_data_list

def generate_report(structure, regulation, context, llm):
   prompt = f"""This is Report Structure from Regulation.
   - Report Structure: {structure}
   - Sample report: {report} from regulation.
   
   Regulation: {regulation}
   Patient chart for Context: {context}

   Kinldy provide a structured report evaluating the patient chart's compliance with this specific regulation.
   Some regulations may require an understading which levels of care the patient was admitted to and through their continuum of care.
   Please focus on the client medical record related items and refrain from including facility / licensing details.

   Kindly compile a comprehensive report of all the findings without conflicting findings. The report needs to be standardized no matter the regulation or insurance guideline and write the page number for reference.

   ## you also need to focus on following things and provide detailed info about one. 
   -Please provide the real page number with analysis the chart regarding to the regulation.
   -Identify the patient's admission date and calculate discrepancy between regulation's admission date and patients's one.
   -Please provide the status of the sign by following sentences in chart
    signed: "FORM SIGNATURES THE FORM HAS BEEN SIGNED"
    not signed: "FORM SIGNATURES"
   -Please provide the real page number of sign missed.
   

   """
   response_text = llm.invoke(prompt).content
   return response_text

############  Extracting content from regulation ##############
regulations_path = "doc/65D-30_Redacted.pdf"
# regulations_documents = LlamaParse(
#             result_type="text"
            
#             ).load_data(regulations_path)


# raw_content = regulations_documents[0].text

# with open('regulation-llama-parse-rawContent.txt', 'w') as file:
#     file.write(str(raw_content))

# regulations_documents = LlamaParse(
#             result_type="markdown"
#             ).load_data(regulations_path)

# raw_content = regulations_documents[0].text

# with open('regulation-llama-parse-instruction.txt', 'w') as file:
#     file.write(str(raw_content))




# keyword = "## 65D"

# data_list = regulations_documents[0].text.split(keyword)[1:]

# regulation = [keyword + data.strip() for data in data_list]
# # print(result)

# with open('regulation-llama-parse.txt', 'w') as file:
#     file.write(str(regulation))

#################### End extracting content from regulation ######################


# split and save the data list check


# pdf_data_list = should_use_ocr("doc/aveatest.pdf")


# with open('pdfDataList.txt', 'w') as file:
#     file.write(str(pdf_data_list))

with open('result_txt/regulation-llama-parse.txt', 'r') as file:
    reg = file.read()
    # print(content)
regulation = eval(reg)
print("-------------------------len of regulation", len(regulation))

QueryList = [
    "65D-30.0041 Clinical Records",
    # "65D-30.0042 Clinical and Medical Guidelines",
    # "65D-30.0043 Placement",
    # "65D-30.0044 Plans, Progress Notes, and Summaries",
    # "65D-30.0045 Rights of Individuals",
    # "65D-30.0049 Voluntary and Involuntary Placement",
    # "65D-30.005 Standards for Addictions Receiving Facilities",
    # "65D-30.006 Standards for Detoxification",
    # "65D-30.0061 Standards for Intensive Inpatient Treatment",
    # "65D-30.007 Standards for Residential Treatment",
    # "65D-30.0081 Standards for Day or Night Treatment with Community Housing",
    # "65D-30.009 Standards for Day or Night Treatment",
    # "65D-30.0091 Standards for Intensive Outpatient Treatment",
    # "65D-30.010 Standards for Outpatient Treatment",
    # "65D-30.011 Standards for Aftercare",
    # "65D-30.012 Standards for Intervention",
    # "65D-30.013 Standards for Prevention",
    # "65D-30.014 Standards for Medication-Assisted Treatment for Opioid Use Disorders",
    # "65D-30.0141 Needs Assessment for Medication-Assisted Treatment for Opioid Use Disorders",
    # "65D-30.0142 Clinical and Operational Standards for Medication-Assisted Treatment for Opioid Use Disorders"
]

with open('pdfDataList.txt', 'r') as file:
    dataList = file.read()


batch_size = 50
dataList = eval(dataList)
print("batch size", len(dataList))
dataList_batches = [dataList[i:i+batch_size] for i in range(0, len(dataList), batch_size)]

report_all_regulations = []
relevant_doc = []

for query in QueryList:
    print("Query", query)
    query = f"Only extract the whole content of {query}."
    reranking = vo.rerank(query, regulation, model="rerank-lite-1", top_k=1)
    result = reranking.results#for r in reranking.results:

    regulation_context = result[0].document

    print("regulation context", regulation_context)

    api_key = os.getenv('OPENAI_API_KEY')
    reg_pmt = """
        This is context that contains regulations(mix of several regulations).
        context: {context}
        From this context, I need to only extract whole content of desired regulation.
        desired regulation: {regulation}
        Extract the whole content of desired regulation.
    """
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=api_key)
    prompt_exp = PromptTemplate(template=reg_pmt, input_variables=["context", "regulation"])
    llm_chain_exp = LLMChain(prompt=prompt_exp, llm=llm)

    reg = query
    correct_reg = llm_chain_exp.run({"context": regulation_context, "regulation": reg})
    
    with open('one_reg.txt', 'w') as file:
        file.write(str(correct_reg))

    for batch in dataList_batches:
        
        query = f"this is regulation, {correct_reg}"
        print(len(batch))
        reranking = vo.rerank(query, batch, model="rerank-lite-1", top_k=30)
        for r in reranking.results:
            relevant_doc.append(r.document)




    print("relevant_doc", len(relevant_doc), "__"*20)
    llm = ChatAnthropic(model="claude-3-opus-20240229", api_key=ANTHROPIC_API_KEY)
    
    with open('relevant_doc.txt', 'w') as file:
        file.write(str(relevant_doc))

#     report = generate_report(samReport, reg, relevant_doc, llm)
#     report_all_regulations.append(report)
#     relevant_doc = []


# with open('report_update.txt', 'w') as file:
#     file.write(str(report_all_regulations))

# txt = ""
# with open('report_update.txt', 'r') as file:
#     report = file.read()
# for report in eval(report):
#     txt += report + "\n\n\n" + "\n" + "___"*30 + "\n\n"

# with open('complete-4-30.txt', 'w') as file:
#     file.write(txt)











    # print(result)

    # with open('correct_regulation.txt', 'w') as file:
    #     file.write(result)


# with open('pdfDataList.txt', 'r') as file:
#     dataList = file.read()


# batch_size = 50
# dataList = eval(dataList)
# print("batch size", len(dataList))
# dataList_batches = [dataList[i:i+batch_size] for i in range(0, len(dataList), batch_size)]

# report_all_regulations = []
# relevant_doc = []
# for reg in regulation:
#     for batch in dataList_batches:
#         query = f"this is regulation, {reg}"
#         print(len(batch))
#         reranking = vo.rerank(query, batch, model="rerank-lite-1", top_k=30)
#         for r in reranking.results:
#             relevant_doc.append(r.document)



#     # print(f"Document: {r.document}")
#     # print(f"Relevance Score: {r.relevance_score}")

#     print("relevant_doc", len(relevant_doc), "__"*20)
#     llm = ChatAnthropic(model="claude-3-opus-20240229", api_key=ANTHROPIC_API_KEY)

#     report = generate_report(samReport, reg, relevant_doc, llm)
#     report_all_regulations.append(report)
#     relevant_doc = []
# with open('report_update.txt', 'w') as file:
#     file.write(str(report_all_regulations))



########## standard report ##################
# txt = ""
# with open('report_update.txt', 'r') as file:
#     report = file.read()
# for report in eval(report):
#     txt += report + "\n\n\n" + "\n" + "___"*30 + "\n\n"

# with open('complete.txt', 'w') as file:
#     file.write(txt)
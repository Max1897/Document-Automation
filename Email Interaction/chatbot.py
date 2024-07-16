from langchain_community.llms import Ollama
import langchain
import prompts as p
from langchain_core.prompts import ChatPromptTemplate
import time

# langchain.debug = True

start = time.time()
llm = Ollama(temperature=0.0, model="llama2")


prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", p.system_prompt1),
        ("human", "{text}"),
    ]
)


prompt = prompt_template.format_messages(
    format_instruction=p.format_instruction, text=p.email3
)
# chain = prompt_template | llm


# response = chain.invoke({"text": email2})

response = llm.invoke("Extract elements from optical character recognition result of a document. \
                       DL is the number after DL. If it starts with 1 then please return it as I \
                      For example, this is an Optical Character Recognition result of a document delimited inside the triple backticks\
```DL 11234568 EXP 08/31/2014 LNCARDHOLDER FN IMA 2570 24TH STREET ANYTOWN, CA 95818 DOB 08131 /1977 RSTR'NON _ OR VEt AN 1```\
                      DL is I1234568 because it is 11234568 in the text which starts with 1, so the actual number should starts with I\
                      Could you please tell me what is the Full name and DL of this document based on this following OCR result? \
                      ``` DL 11234562 ExP 08/31/2015 LN Alex FN John 2570 24TH STREET SACRAMENTO, CA 95818 DOB 08/31/1977 RSTR NONE ```")

# output_dict = p.output_parser.parse(response)


print(response)

time_used = time.time() - start
print(f"Time used:{time_used:.2f} s")

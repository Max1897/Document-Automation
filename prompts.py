from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

# Parser
intention_schema = ResponseSchema(
    name="Intention",
    description="Is the intention of this text sender trying to make a loan? \
                                  Answer Loan Application if Yes. Answer Not Clear if No",
)
loan_amt_schema = ResponseSchema(
    name="Amount",
    description="If the text sender wants to make a loan, what is the exact amount \
                                 of loan he or she wants to make. Answer the exact number of the amount. If the text sender does \
                                 not want to make a loan, answer N/A",
)
income_schema = ResponseSchema(
    name="Income",
    description="If the text send shows how much his or her income is. Answer the number of it. \
                               Otherwise answer N/A",
)
file_schema = ResponseSchema(
    name="File uploaded",
    description="If the text says he or she has upload needed files. Answer True if yes. \
                             Answer False if no.",
)

response_schemas = [intention_schema, loan_amt_schema, income_schema, file_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instruction = output_parser.get_format_instructions()

# System
system_prompt1 = "You are a loan application processing bot, you will receive text \
from people who want to make a loan. Extract certain informations from the text you receive. \
    Follow the following instructions.  \
     {format_instruction} "

system_prompt2 = "You are a helpful bot."

#Input text
email1 = "I hope this email finds you well. I am writing to express my interest in applying \
for a loan from the Bank of China. After carefully reviewing your lending \
options and considering my financial needs, I believe that your institution aligns \
perfectly with my requirements."

email2 = "I had some noodles, very delicious!"

email3 = "I am writing to express my interest in securing a loan to support my home renovation project. \
    After careful consideration of my financial situation, I am seeking a loan of $15,000 to cover the necessary expenses. \
Currently, my monthly income stands at $3,500, which I believe adequately supports the repayment of the \
    loan within the agreed terms. Furthermore, I have completed the upload of all required financial files, \
including recent pay stubs, bank statements, and proof of residence, to facilitate the loan application process. \
Thank you for considering my request, and I look forward to discussing the details further."

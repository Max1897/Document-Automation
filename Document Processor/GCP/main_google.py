'''
GCP Document AI main
'''

import json
import time
from process import process_document



classifier_id = "8f37c0bc1d662419"
classifier_version_id = "4249aa4dd54b9e2a"
extractor_id = "cdc3fbed02a7886"
extractor_version_id = "c88ea2732bd0382d"


project_id = "docauto-410203"
location = "us"  # Format is "us" or "eu"
processor_id = "cdc3fbed02a7886"  # Create processor before running sample
file_path = "raw data\JP DL Back.jpg"
# Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
# mime_type = "application/pdf"
mime_type = "image/jpeg"
# Optional. The fields to return in the Document object.
field_mask = "text,entities,pages.pageNumber"
processor_version_id = ""  # Optional. Processor version to use
page_process = 1  # Select page to process, start from 1

start = time.time()

# # Classify document
# document_classification = process_document(
#     project_id, location, classifier_id, file_path, mime_type, field_mask, classifier_version_id
# )
# max_con = 0
# classification = ""
# for i in document_classification.entities:
#     if i.confidence > max_con:
#         classification = i.type_

# print("Document Classification:", classification)

# Extract selected items
document = process_document(
    project_id, location, extractor_id, file_path, mime_type, field_mask, extractor_version_id
)

JSON_output = {}
# JSON_output["File_type"] = classification
JSON_output["Extracted"] = {}
for i in document.entities:
    JSON_output["Extracted"][i.type_] = i.mention_text

end = time.time()
print(JSON_output)
print("Time used:", end - start)
with open("output.json", "w") as outfile:
    json.dump(JSON_output, outfile)

# print(document)

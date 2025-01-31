# Source od code
# https://docs.aws.amazon.com/textract/latest/dg/examples-extract-kvp.html

import boto3
import sys
import re
import json
import time
from collections import defaultdict


def get_kv_map(file_name):
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded', file_name)

    # process using image bytes
    session = boto3.Session(profile_name='default')
    client = session.client('textract', region_name='us-east-2')
    response = client.analyze_document(Document={'Bytes': bytes_test},
                                       QueriesConfig={
        'Queries': [
            {
                'Text': 'What is employee\'s first name and initial',
            },
        ]
    },
        FeatureTypes=['TABLES', 'FORMS', 'LAYOUT','QUERIES'],
    #     AdaptersConfig={
    #     'Adapters': [
    #         {
    #             'AdapterId': 'ca5011d20a5d',
    #             'Pages': [
    #                 '1',
    #             ],
    #             'Version': '1'
    #         },
    #     ]
    # }
    )

    # Get the text blocks
    blocks = response['Blocks']
    

    # get key and value maps
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block

    return key_map, value_map, block_map


def get_kv_relationship(key_map, value_map, block_map):
    kvs = defaultdict(list)
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key].append(val)
    return kvs


def find_value_block(key_block, value_map):
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '

    return text


def print_kvs(kvs):
    for key, value in kvs.items():
        print(key, ":", value)


def search_value(kvs, search_key):
    for key, value in kvs.items():
        if re.search(search_key, key, re.IGNORECASE):
            return value


def main(file_name):
    key_map, value_map, block_map = get_kv_map(file_name)

    # Get Key Value relationship
    kvs = get_kv_relationship(key_map, value_map, block_map)
    print("\n\n== FOUND KEY : VALUE pairs ===\n")
    print_kvs(kvs)

    # Start searching a key value
    # while input('\n Do you want to search a value for a key? (enter "n" for exit) ') != 'n':
    #     search_key = input('\n Enter a search key:')
    #     print('The value is:', search_value(kvs, search_key))

    with open("output.json", "w") as outfile:
        json.dump(kvs, outfile)


if __name__ == "__main__":
    start = time.time()
    file_name = 'raw data\Pay Stubs - 3-images-1 (1).jpg'
    main(file_name)
    end = time.time()
    print("Time used:{:2f} seconds".format(end - start))

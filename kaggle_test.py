import os
import csv
import json

def metadata_extracter(pages_to_loop=100, path="/Users/hanley/Desktop/SI_650_Group_Project/SI_650_Group_Project"):

    '''
    1) grab username/dataset info
    2) use the username/dataset info to retrieve metadata
    3) parse metadata for 'description', 'title', 'subtitle', 'description'
    '''
    print('saving data in {}'.format(path))

    json_dataset = {}

    ### fetch username/dataset
    for page_num in range(pages_to_loop):
        csv_command = 'kaggle datasets list -p{} --csv > dataset_name.csv'.format((page_num+1), path)
        os.system(csv_command)

        ### parse 'ref' from csv
        # ref should look like kmader/skin-cancer-mnist-ham10000
        filepath = '{}/dataset_name.csv'.format(path)
        ref_list = []
        with open(filepath, 'r') as f:
            ref_csv = csv.DictReader(f)
            for row in ref_csv:
                # print(row)
                ref_list.append(row['ref'])

        ### download the metadata using key_info into the path of your choice
        for idx, each_ref in enumerate(ref_list):
            json_command = 'kaggle datasets metadata {} -p "{}"'.format(each_ref, path)
            os.system(json_command)

            ### read through json file downloaded to grab the following:
            # title
            # subtitle
            # description
            # keywords

            json_path = '{}/dataset-metadata.json'.format(path)
            fileToUse = open(json_path)
            dataset_json = json.load(fileToUse)

            ### parse json
            json_dataset[idx] = {
                'title': dataset_json['title'],
                'subtitle': dataset_json['subtitle'],
                'description': dataset_json['description'],
                'keywords': dataset_json['keywords']
            }

    ## save dictionary as csv?
    with open('{}/dataset.csv'.format(path), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'subtitle', 'description', 'keywords'])
        print(json_dataset)
        for i in json_dataset:
            writer.writerow(
                [json_dataset[i]['title'],
                json_dataset[i]['subtitle'],
                json_dataset[i]['description'],
                json_dataset[i]['keywords']
            ])

if __name__ == '__main__':
    metadata_extracter(pages_to_loop=1)

import os
import csv
import json
import sys

akio_path = "C:/Users/akiok/Google Drive/MSI/SI650/project/SI_650_Group_Project"
liz_path = "/Users/hanley/Desktop/SI_650_Group_Project/SI_650_Group_Project"
amy_path = ''

def metadata_extracter(path, pages_to_loop=100):

    '''
    1) grab username/dataset info
    2) use the username/dataset info to retrieve metadata
    3) parse metadata for 'description', 'title', 'subtitle', 'description'
    '''
    print('saving data in {}'.format(path))

    json_dataset = {}
    counter = 0

    ### fetch username/dataset
    for page_num in range(pages_to_loop):
        csv_command = 'kaggle datasets list -p{} --csv > dataset_name.csv'.format((page_num+1), path)
        os.system(csv_command)

        ### parse 'ref' from csv
        # ref should look like kmader/skin-cancer-mnist-ham10000
        filepath = '{}/dataset_name.csv'.format(path)
        ref_list = []
        with open(filepath, 'r', newline='') as f:
            ref_csv = csv.DictReader(f)
            for row in ref_csv:
                # print(row)
                ref_list.append(row['ref'])
        print("\nreflist: {}\n".format(ref_list))
        ### download the metadata using key_info into the path of your choice
        for each_ref in ref_list:
            json_command = 'kaggle datasets metadata {} -p "{}"'.format(each_ref, path)
            os.system(json_command)

            ### read through json file downloaded to grab the following:
            # title
            # subtitle
            # description
            # keywords

            json_path = '{}/dataset-metadata.json'.format(path)
            fileToUse = open(json_path, encoding = 'utf-8')
            dataset_json = json.load(fileToUse)

            ### parse json
            json_dataset[counter] = {
                'title': str(dataset_json['title']).encode('utf-8'),
                'subtitle': str(dataset_json['subtitle']).encode('utf-8'),
                'description': str(dataset_json['description']).encode('utf-8'),
                'keywords': str(dataset_json['keywords']).encode('utf-8')
            }
            counter+=1
            print(counter)

    ## save dictionary as csv?
    with open('{}/dataset.csv'.format(path), 'w', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(['title', 'subtitle', 'description', 'keywords'])
        print(json_dataset)
        for i in json_dataset:
            writer.writerow([
                json_dataset[i]['title'],
                json_dataset[i]['subtitle'],
                json_dataset[i]['description'],
                json_dataset[i]['keywords']
            ])

if __name__ == '__main__':
    try:
        path = str(sys.argv[1])
        pages = str(sys.argv[2])
        # print("path: {}\npages: {}".format(path, pages))
        metadata_extracter(path=akio_path, pages_to_loop=1)
    except:
        metadata_extracter(path=akio_path, pages_to_loop=1)

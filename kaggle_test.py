import os
import csv
import json

def metadata_extracter(pages_to_loop=100, path="C:/Users/akiok/Google Drive/MSI/SI650/project/SI_650_Group_Project"):

    '''
    1) grab username/dataset info
    2) use the username/dataset info to retrieve metadata
    3) parse metadata for 'description', 'title', 'subtitle', 'description'
    '''


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
                ref_list.append(row['ref'])

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
            json.load(json_path)


            ### parse json and save as dictionary

    ### save dictionary as csv?



if __name__ == '__main__':
    metadata_extracter(pages_to_loop=1)

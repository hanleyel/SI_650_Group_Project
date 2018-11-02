import os

def metadata_extracter(path="C:/Users/akiok/Google Drive/MSI/SI650/project/SI_650_Group_Project"):

    '''
    1) grab username/dataset info
    2) use the username/dataset info to retrieve metadata
    3) parse metadata for 'description'
    '''


    ### fetch username/dataset
    command = 'kaggle datasets list -p1 --csv'
    os.system(command)

    ### save into csv


    ### parse key info, aka 'ref'
    # should look like kmader/skin-cancer-mnist-ham10000
    key_info = 'kmader/skin-cancer-mnist-ham10000'

    ### download the metadata using key_info into the path of your choice
    command = 'kaggle datasets metadata {} -p "{}"'.format(key_info, path)
    os.system(command)

    ### read through json file downloaded

    ### parse json for 'description' and save as csv


if __name__ == '__main__':
    metadata_extracter()

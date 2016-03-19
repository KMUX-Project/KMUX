import json
import os


class Util:
    @staticmethod
    def readJSONFile(filename):
        '''
        Serialize a JSON file in the form of a dictionary
        :return: the dictionary that represents the JSON file
        '''
        f = open(os.environ['PYTHONPATH'] + "/" + filename)
        return json.load(f)

    @staticmethod
    def writeToSONFile(filename, dict):
        fp = open(os.environ['PYTHONPATH'] + "/" + filename)
        json.dump(dict,fp, indent=True)
import json
import os


class Json:

    @staticmethod
    def readJSONFile(filename):
        '''
        Serialize a JSON file in the form of a dictionary
        :return: the dictionary that represents the JSON file
        '''
        f = open(filename)
        return json.load(f)

    @staticmethod
    def writeToJSONFile(filename, dict):
        fp = open(filename)
        json.dump(dict, fp, indent=True)

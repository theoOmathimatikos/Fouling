import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class NavalBrain():

    def __init__(self,
                 key=None, 
                 templ='chat', 
                 model='gpt-3.5-turbo-0125', 
                 parse="str"):

        self._init_key(key)

        self.prompt = self._construct_prompt()

        self.templ = templ
        self.model = model
        self.parse = parse

        self._set_llm()


    def _init_key(self, key):

        if key==None:
            with open("keys.json") as keys:
                use_key = json.load(keys)["key"]
        else:
            use_key = key

        os.environ["OPENAI_API_KEY"] = use_key


    def _set_prompt_temp(self):

        if self.templ == 'chat':
            self.prompt_temp = ChatPromptTemplate.from_messages([
                ("system", self.prompt['general']),
                ("user", self.prompt['specific']),
                ("system", self.prompt['summary']),
                ("user", self.prompt['data_struct']),
                ("user", self.prompt['data'])
            ])
            
    def _set_model(self):

        self.llm = ChatOpenAI(model=self.model)

    def _set_parser(self):

        if self.parse == 'str':
            self.parser = StrOutputParser() 
    
    def _set_llm(self):

        self._set_prompt_temp()
        self._set_model()
        self._set_parser()

        self.model = self.prompt_temp | self.llm | self.parser

    
    def _construct_prompt(self):

        return {'general': """ 
                  <role> 
                  You are a helpful naval engineer whose job is to summarise data extracted from the vessel's crew. 
                  The specific situation of the vessel that you will construct the summary on is the following:
                  </role> \n\n
                  """,

                  'specific': """
                  <specific>
                  {specific}
                  </specific> \n\n
                  """,

                  'summary': """
                  <summary>
                  You make a brief summary of the data, provided by the user below. The style of the text should 
                  be in accordance with your role. The responce, should be brief, expressed in a few sentences and without 
                  many explanations. There is no need to explain any acronyms. Also, if no data is provided from the user,
                  answer 'No data provided to make any suggestion.'. 
                  </summary> \n\n
                  """,

                  'data_struct': """
                  <data_structure>
                  {data_structure}
                  </data_structure> \n\n
                  """,

                  'data': """
                  <data>
                  {data}
                  </data>
                  """}
    
    def data_structure(self, data):

        if type(data) == dict:
            data_struct = """ 
                The data that are provided by the user are given as a list of features. The names of the features 
                characterise the features themselves. E.g. the feature 'speed' corresponds to the speed of the vessel. \n
                """
        else:
            data_struct = """ 
                The data that are provided by the user are given as a dictionary of key-value pairs, with keys 
                and values representing the features and their values respectively. The names of the features 
                characterise the features themselves. E.g. the feature 'speed' corresponds to the speed of the vessel.\n
                """
        return data_struct


    def invoke(self, specific, params, data):

        data = zip_data(params, data)

        data_struct = self.data_structure(data)

        answer = self.model.invoke({
            "specific": specific, 
            "data_structure": data_struct, 
            "data": data
        })

        return answer
    

def zip_data(params, data):

    data = str(params) if data == None else str({k:v for (k, v) in zip(params, data)})
    return data



if __name__ == "__main__":

    specific = "The vessel operates outside its usual operating profile."
    params = ["speed", "fuel_burn", "speed_limit", "fuel_burn_limit"]
    data = ["15", "14000", "10", "10000"]

    ans = NavalBrain().invoke(specific, params, data)
    print(ans)

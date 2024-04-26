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
                ("system", self.prompt['data_struct']),
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
                  redundant explanations. Start the sentences directly, without saying 'as per the provided data'
                  or anything similar. There is no need to explain any acronyms. 
                  
                  Also, if no data is provided from the user, answer 'No data provided to make any suggestion.'. 
                  </summary> \n\n
                  """,

                  'data_struct': """
                  <data_structure>
                  The data that are provided by the user are given as a dictionary of key-value pairs, with keys 
                  and values representing the features and their values respectively. Sometimes the key will be 
                  associated with a unique value, while in other cases a key might correspond to a list of values. 
                  The names of the features characterise the features themselves.\n
                  E.g. the feature 'speed' corresponds to the speed of the vessel.\n
                  </data_structure> \n\n
                  """,

                  'data': """
                  <data>
                  {data}
                  </data>
                  """}


    def invoke(self, specific, data):

        answer = self.model.invoke({
            "specific": specific, 
            "data": data
        })

        return answer


if __name__ == "__main__":

    # specific = "The vessel operates outside its usual operating profile."
    # data = str({"speed": "15 kn", "speed_limit": "10 kn", "fuel_burn": "14000 gal", "fuel_burn_limit": "10000 gal"})

    specific = "The vessel is armed with Antifouling Coating. The different substances are provided."
    data = str({"substances": ["SPC", "CBD", "Insoluble Matrix"]})

    ans = NavalBrain().invoke(specific, data)
    print(ans)

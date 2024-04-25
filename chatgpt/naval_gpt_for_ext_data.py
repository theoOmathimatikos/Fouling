from chatgpt.naval_gpt import NavalBrain

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain


class NavalBrainExtData(NavalBrain):

    def __init__(self, 
                 key=None, 
                 templ='chat', 
                 model='gpt-3.5-turbo-0125', 
                 parse="str", 
                 vectorstore="FAISS"):

        super().__init__(key, templ, model, parse)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = vectorstore

    
    def _construct_prompt(self):

        super()._construct_prompt()

        self.prompt["ext_data_expl"] = """ 
            <external_data>
            I provide you the following data that are specific to our situation, in order for you to make a better judgement. \n\n 
            </external_data>
        """ 
        self.prompt["ext_data"] = """ 
            <data>
            {ext_data}
            </data>
        """
        
    
    def _set_prompt_temp(self):

        if self.templ == 'chat':
            self.prompt_temp = ChatPromptTemplate.from_messages([
                ("system", self.prompt['general']),
                ("user", self.prompt['specific']),
                ("system", self.prompt['summary']),
                ("user", self.prompt['data_struct']),
                ("user", self.prompt['data']),
                ("system", self.prompt['ext_data_expl']),
                ("user", self.prompt["ext_data"])
            ])


    def feed_web_data(self, webpage):
        "It might be useful in cases where there is data in the web about a particular component of the vessel, e.g. AFC"
        
        loader = WebBaseLoader(webpage)
        docs = loader.load()
        return docs
    
    
    def save_data_in_vectorstore(self, ext_data):

        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(ext_data)
        if self.vectorstore == "FAISS":
            vector = FAISS.from_documents(documents, self.embeddings)
        return vector


    def prompt_with_retrieval(self, ext_data):

        vector = self.save_data_in_vectorstore(ext_data)

        document_chain = create_stuff_documents_chain(self.model, self.prompt)
        retriever = vector.as_retriever()

        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        return retrieval_chain
    

    def invoke_retrieval_chain(self, specific, data, ext_data):

        data_struct = super().data_structure(data)
        retrieval_chain = self.prompt_with_retrieval(ext_data)

        response = retrieval_chain.invoke({
            "specific":specific, 
            "data_structure": data_struct, 
            "data": data,
            "ext_data": ext_data
        })

        return response["answer"]
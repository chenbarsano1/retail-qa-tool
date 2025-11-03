import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit

from few_shots import few_shots

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def get_few_shot_sql_agent():
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_port = "3307"
    db_name = "atliq_tshirts"

    db = SQLDatabase.from_uri(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
        sample_rows_in_table_info=3
    )


    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.1)


    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)


    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )


    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix="You are a MySQL expert. Use the following examples to guide your SQL query generation.",
        suffix="\nNow answer this question:\nQuestion: {input}\nSQLQuery:",
        input_variables=["input"],
    )


    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()


    system_prompt = f"""
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {db.dialect} query to run,
then look at the results of the query and return the answer.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

Here are some few-shot examples of questions, SQL, results, and answers:
{few_shot_prompt.format(input="")}

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.
"""
    
    llm_with_tools = llm.bind_tools(tools)

    agent = create_agent(
        llm_with_tools,
        tools,
        system_prompt=system_prompt
    )


    return agent

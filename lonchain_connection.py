import mysql.connector as sql
from langchain_google_genai import GoogleGenerativeAI
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.prompts import SemanticSimilarityExampleSelector, FewShotPromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate

from few_shots import few_shots
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

mydb = sql.connect(
    host="localhost",
    user="root",
    password="",
    database="online_store"
)

engine = create_engine('mysql+mysqlconnector://root:@localhost/online_store')
SECRET_KEY = "My  Secret Key "


def format_response(sql_result):
    headers = sql_result.keys()
    rows = sql_result.fetchall()
    table = "\n".join([", ".join(headers)] + [", ".join(map(str, row)) for row in rows])
    return f"Table format:\n{table}\n"


def get_few_shot_db_chain():
    db = SQLDatabase(engine)
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=SECRET_KEY, temperature=0.1)
    #llm = GoogleGenerativeAI(google_api_key="AIzaSyAyD-fzPLMtBx4GK4J9HWHn-Mqi77In3GU", temperature=0.1)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=1,
    )
    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".

    Use the following format:

    Question: Question here
    SQLQuery: Query to run with no pre-amble
    SQLResult: Result of the SQLQuery
    Answer: Final answer here

    No pre-amble.
    """

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer", ],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
    # chain.format_response = format_response
    return chain



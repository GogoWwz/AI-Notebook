from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, MarkdownHeaderTextSplitter
import os

os.environ["OPENAI_API_KEY"] = "xxx"

# 创建embedding（基于openai）
embeddings = OpenAIEmbeddings()

# 加载文档（具体路径环境不同，不必完全一致）
current_dir = os.getcwd()
loader1 = TextLoader(os.path.join(current_dir, 'dataconnection/dataset/q1.css盒模型.txt'), encoding='utf8')
loader2 = TextLoader(os.path.join(current_dir, 'dataconnection/dataset/q2.基本数据类型.txt'), encoding='utf8')
md_loader = TextLoader(os.path.join(current_dir, 'dataconnection/dataset/q1.前端基础.md'), encoding='utf8')

doc1 = loader1.load()
doc2 = loader2.load()
md_doc = md_loader.load()

headers_to_split_on = [
  ("#", "前端基础"),
  ("##", "基础类目"),
  ("###", "具体题目"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_docs = markdown_splitter.split_text(md_doc[0].page_content)
print(md_docs)
print(len(md_docs))


# 创建splitter
splitter = RecursiveCharacterTextSplitter(
  chunk_size = 100,
  chunk_overlap  = 20,
  length_function = len,
)

docs = splitter.split_documents(doc1 + doc2)
print(docs)
print(len(docs))

# 将文档生成向量存储
vectorstore = Chroma.from_documents(docs, embeddings)

# 生成检索器
retriever = vectorstore.as_retriever(search_kwargs={
  "k": 5,
})

# 查询
interviewer_answers = """
  css盒模型我只知道标准盒模型和怪异盒模型，其他不是很清楚
"""
res = retriever.get_relevant_documents(interviewer_answers)
print(res)
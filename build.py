import json
from neo4j import GraphDatabase
import logging

import pyfiglet
import pyfiglet


#  启动文字设置
#https://www.asciiart.eu/animals/frogs
def print_program_name(name):
    # Convert the program name into ASCII art using a slanted font
    ascii_art_name = pyfiglet.figlet_format(name, font="slant")
    print(ascii_art_name)

    # ASCII art drawing
ascii_drawing = """
--graphRAG-- 

 Art by Joan Stark
         _ _
        (oTo)
     _.-( _ )-._
    `/`( '-' )`\`
       /'---'\
     __\     /__
jgs  \_/     \_/
"""
print(ascii_drawing)

# Call the function with the name of your program



# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 连接到 Neo4j 数据库
uri = "bolt://localhost:7687"
username = "neo4j"
password = "txys6666"
driver = GraphDatabase.driver(uri, auth=(username, password))
logging.info("已连接到  数据库，地址：%s，使用用户名：%s", uri, username)

# 读取 JSON 数据
with open("company_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    logging.info("JSON 数据加载成功，共有 %d 家公司，%d 条关系", len(data["companies"]), len(data["relationships"]))

# 定义 Cypher 查询语句
cypher_create_node = """
    UNWIND $companies AS company
    CREATE (c:Company)
    SET c.name = company.name,
        c.type = company.type,
        c.size = company.size,
        c.address = company.address,
        c.founded = company.founded,
        c.business_area = company.business_area
"""
cypher_create_relationship = """
    UNWIND $relationships AS rel
    MATCH (source:Company {name: rel.source}), (target:Company {name: rel.target})
    CREATE (source)-[:guanxi]->(target)
"""

# 执行 Cypher 查询
def execute_query(tx, cypher_query, data):
    result = tx.run(cypher_query, **data)
    #logging.info("已执行 Cypher 查询，涉及数据：%s", data)
    return result

with driver.session() as session:
    # 执行创建节点的查询
    nodes_result = session.execute_write(execute_query, cypher_create_node, {"companies": data["companies"]})
    logging.info("已创建公司节点")

    # 执行创建关系的查询
    relationships_result = session.execute_write(execute_query, cypher_create_relationship, {"relationships": data["relationships"]})
    logging.info("已创建公司间的关系")

# 关闭数据库连接
driver.close()
logging.info("已关闭 Neo4j 数据库连接")

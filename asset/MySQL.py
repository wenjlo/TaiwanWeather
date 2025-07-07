import pandas as pd
import mysql.connector
from datetime import datetime
from config import DB_USER,DB_PASSWORD,DB_IP
from sqlalchemy import create_engine
import os


def insert_with_ignore(table, conn, keys, data_iter):
    """
    自訂插入方法，使用 MySQL 的 INSERT IGNORE 語法。
    這會忽略任何導致唯一索引衝突的行。

    Args:
        table (sqlalchemy.Table): 目標資料表的 SQLAlchemy Table 物件。
        conn (sqlalchemy.engine.Connection): SQLAlchemy 連線物件。
        keys (list): DataFrame 的欄位名稱列表。
        data_iter (iterator): 包含要插入資料行（元組）的迭代器。
    """
    # 建立一個列表來儲存要插入的欄位名稱
    columns = ', '.join(f"`{k}`" for k in keys)  # 使用反引號確保欄位名稱正確
    # 建立一個列表來儲存值的佔位符
    values_placeholder = ', '.join(['%s'] * len(keys))

    # 組合 INSERT IGNORE 語句
    sql = f"INSERT IGNORE INTO `{table.name}` ({columns}) VALUES ({values_placeholder})"

    # 執行批量插入
    # 當使用 SQLAlchemy 的 to_sql 方法時，傳入的 conn 物件是 SQLAlchemy 的 Connection，
    # 而不是底層的 DB-API 連線。需要透過 conn.connection 才能取得 DB-API 連線物件，
    # 進而呼叫其 cursor() 和 commit() 方法。
    cursor = conn.connection.cursor()
    # 修正點：將 data_iter 轉換為列表，以符合 executemany 的參數要求
    cursor.executemany(sql, list(data_iter))
    conn.connection.commit()
    print(f"  -> 插入完成，忽略重複的主鍵資料。實際影響行數: {cursor.rowcount}")



class Mysql:
    def __init__(self):

        self.db_config = {
            'host': DB_IP,  # 如果是透過 kubectl port-forward 連接，則為 127.0.0.1
            'port': 3306,  # 如果是透過 kubectl port-forward 連接，則為 3306
            'user': DB_USER,  # 您的 MySQL 用戶名
            'password': os.environ.get("MYSQL_PASSWORD"),  # 您的 MySQL 密碼
            'database': None  # 您的資料庫名稱
        }
        self.ip = DB_IP
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.db = None


    def write(self, data_frame,table_name,target_db):
        self.db = target_db
        self.db_config['database'] = target_db
        engine = create_engine(
            f"mysql+mysqlconnector://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        )

        with engine.connect() as connection:
            print("成功連線到 MySQL 資料庫。")

        print("開始 插入資料 (帶有 INSERT IGNORE)...")
        data_frame.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',  # 這裡的 'append' 只是 to_sql 的一個要求，實際行為由 method 決定
            index=False,
            method=insert_with_ignore  # 指定我們自訂的插入方法
        )

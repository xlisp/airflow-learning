#!/bin/bash

# 设置Airflow环境变量
export AIRFLOW_HOME=~/airflow

# 初始化Airflow数据库
airflow db init

# 创建DAGs文件夹（如果不存在）
mkdir -p $AIRFLOW_HOME/dags

# 复制我们的脚本和配置到DAGs文件夹
cp json_to_dag.py $AIRFLOW_HOME/dags/
cp dag_config.json $AIRFLOW_HOME/dags/

# 创建Airflow用户（首次使用时需要）
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# 启动Airflow WebServer（在后台运行）
airflow webserver -p 8080 &

# 启动Airflow调度器（在后台运行）
airflow scheduler &

echo "Airflow已启动！"
echo "请在浏览器中访问 http://localhost:8080 查看DAG"
echo "用户名: admin  密码: admin"

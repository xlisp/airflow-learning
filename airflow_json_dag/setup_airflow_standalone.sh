#!/bin/bash

# 设置Airflow环境变量
export AIRFLOW_HOME=~/airflow

# 确保目录存在
mkdir -p $AIRFLOW_HOME/dags

# 复制我们的脚本和配置到DAGs文件夹
cp json_to_dag.py $AIRFLOW_HOME/dags/
cp dag_config.json $AIRFLOW_HOME/dags/

# 初始化Airflow数据库
airflow db migrate

# 启动Airflow standalone模式
# 在最新版本的Airflow中，standalone模式会自动启动webserver, scheduler和其他必要组件
echo "正在启动Airflow standalone模式..."
echo "首次运行时，系统会要求您创建一个管理员用户"
echo "启动后，请访问 http://localhost:8080 查看DAG"

# 启动standalone模式
airflow standalone

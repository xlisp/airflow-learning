import json
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

# 默认参数
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_dag_from_json(json_file_path):
    """从JSON文件加载DAG配置"""
    with open(json_file_path, 'r') as file:
        dag_config = json.load(file)
    
    # 创建DAG
    dag_id = dag_config.get('dag_id', 'json_generated_dag')
    dag_desc = dag_config.get('description', 'DAG generated from JSON')
    schedule = dag_config.get('schedule_interval', None)
    
    dag = DAG(
        dag_id,
        default_args=default_args,
        description=dag_desc,
        schedule_interval=schedule,
        catchup=False,
    )
    
    # 创建任务
    tasks = {}
    for task_config in dag_config.get('tasks', []):
        task_id = task_config.get('task_id')
        task_type = task_config.get('type', 'bash')
        
        if task_type == 'python':
            # 定义Python函数
            def task_function(**kwargs):
                print(f"执行任务 {kwargs['task_id']}")
                # 这里可以根据JSON中的配置执行不同的操作
                return f"任务 {kwargs['task_id']} 完成"
            
            task = PythonOperator(
                task_id=task_id,
                python_callable=task_function,
                op_kwargs={'task_id': task_id},
                dag=dag,
            )
        elif task_type == 'bash':
            task = BashOperator(
                task_id=task_id,
                bash_command=task_config.get('bash_command', 'echo "执行 ${task_id}"'),
                dag=dag,
            )
        else:
            # 默认使用空操作符
            task = EmptyOperator(
                task_id=task_id,
                dag=dag,
            )
        
        tasks[task_id] = task
    
    # 设置任务依赖关系
    for task_config in dag_config.get('tasks', []):
        task_id = task_config.get('task_id')
        dependencies = task_config.get('dependencies', [])
        
        for dep in dependencies:
            if dep in tasks and task_id in tasks:
                tasks[dep] >> tasks[task_id]
    
    return dag

# 将此DAG添加到Airflow
def create_dag_from_json(json_file_path):
    """创建一个可以被Airflow识别的DAG对象"""
    dag = load_dag_from_json(json_file_path)
    globals()[dag.dag_id] = dag
    return dag

# 指定JSON文件路径
# 将此路径替换为您的JSON文件的实际路径
json_file_path = os.path.join(os.path.dirname(__file__), 'dag_config.json')

# 如果文件存在，创建DAG
if os.path.exists(json_file_path):
    dag = create_dag_from_json(json_file_path)


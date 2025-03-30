## airflow 跑一个依赖任务编写: 
```
a -> b -> c;
a -> d;
b -> e
```
---

我将帮你编写一个Airflow DAG，其中包含任务依赖关系：a -> b -> c, a -> d, b -> e。这是一个完整的Airflow DAG实现：

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# 默认参数
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 30),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 创建DAG
dag = DAG(
    'task_dependencies_example',
    default_args=default_args,
    description='简单的任务依赖DAG示例',
    schedule_interval=timedelta(days=1),
)

# 定义任务函数
def task_a(**kwargs):
    print("执行任务 A")
    return "任务 A 完成"

def task_b(**kwargs):
    print("执行任务 B")
    return "任务 B 完成"

def task_c(**kwargs):
    print("执行任务 C")
    return "任务 C 完成"

def task_d(**kwargs):
    print("执行任务 D")
    return "任务 D 完成"

def task_e(**kwargs):
    print("执行任务 E")
    return "任务 E 完成"

# 创建任务
task_a = PythonOperator(
    task_id='task_a',
    python_callable=task_a,
    dag=dag,
)

task_b = PythonOperator(
    task_id='task_b',
    python_callable=task_b,
    dag=dag,
)

task_c = PythonOperator(
    task_id='task_c',
    python_callable=task_c,
    dag=dag,
)

task_d = PythonOperator(
    task_id='task_d',
    python_callable=task_d,
    dag=dag,
)

task_e = PythonOperator(
    task_id='task_e',
    python_callable=task_e,
    dag=dag,
)

# 设置依赖关系
# a -> b -> c
task_a >> task_b >> task_c
# a -> d
task_a >> task_d
# b -> e
task_b >> task_e
```

这个DAG实现了你指定的依赖关系：
- 任务A完成后，任务B和任务D开始执行
- 任务B完成后，任务C和任务E开始执行

注意：我使用了PythonOperator作为示例，你可以根据实际需求替换为其他类型的Operator，例如BashOperator、SqlOperator等。

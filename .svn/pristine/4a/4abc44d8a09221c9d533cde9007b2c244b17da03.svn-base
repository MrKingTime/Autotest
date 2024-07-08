## UI 自动化模板

### 项目架构

##### 主体思路

> ###### 框架
>
> 使用 pytest 管理用例：用例维度分为用例集->单条用例
> selenium 操作元素：action 中二次封装元素操作
> allure 生成报告：jenkins 中生成查看 allure 报告
> liunx 部署远程分布式服务：docker 部署远程分布式服务，远程执行
> jenkins 集成执行：jenkins 远程执行任务，并在 jenkins 中生成 allure 报告

> ###### 介绍
>
> 测试用例集中存放多条用例，用例调用页面对象中封装的功能的操作步骤
>
> UI 自动化仅保证主流程且正向用例的功能覆盖，其他功能及方向用例使用接口自动化实现（因为编写 UI 自动化比接口自动化复杂，成本大，且会有网络、兼容性等因素影响稳定性）
>
> 执行过程->http://xxx/vnc.html # 密码是 secret
> 报告查看->http://xxx/job/allure-report/allure/

##### 运行库

> python = "^3.8"
> pytest = "7.3.1"
> selenium = "4.9.0"
> pytest-dependency = "0.5.1"
> pytest-rerunfailures = "11.1.2"
> allure-python-commons = "2.13.2"
> allure-pytest = "2.13.2"
> pytest-ordering = "0.6"
> pytest-sugar = "0.9.7"
> requests = "^2.31.0"

### 项目准备

> conda create --name interface-auto python=3.11.1
> activate interface-auto
> pip install -r requirements.txt

### 项目运行

> python main.py

### 目录结构

> ├─.venv # 虚拟环境
> ├─action # slenium 操作封装
> ├─allure # 报告
> ├─driver # driver 管理
> ├─logs # 日志
> ├─pages # 页面对象，包含页面上获取元素的方法和组合操作
> ├─testcase # 测试用例集
> ├─testdata # 测试数据
> ├─tools # 工具函数
> │ .gitignore # git
> │ constant.py # 常量
> │ main.py # 主函数，执行文件来启动 pytest，而不是命令行，方便配置
> │ poetry.lock # 环境版本映射
> │ pyproject.toml # 包管理
> │ pytest.ini # pytest 配置
> │ README.md
> │ 测试用例.puml

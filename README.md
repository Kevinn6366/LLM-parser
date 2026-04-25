


## 🛠️ 环境准备

在开始运行项目之前，请确保你的开发环境已安装 Python 3.8+ 和 Node.js 16+。

### 1. 后端配置 (Flask)

首先，你需要创建一个虚拟环境并配置 Dify 相关的环境变量。

1. **创建虚拟环境**:
 
  

 创建环境
>    python -m venv env


2.安装依赖


> pip install -r requirements.txt

3.配置环境变量:
在项目根目录下创建一个 .env 文件（或直接在系统环境中设置），并填写你的 Dify 配置：



> DIFY_API_KEY=your_api_key_here
> DIFY_URL=your_dify_base_url_here
注意：app.py 会通过 os.getenv 自动读取这些配置。




### Dify 部署参考
关于 Dify 端的 Workflow 或 Agent 配置，可以参考项目根目录下的：

- DifyNode.png: 节点编排示意图

- Algorithm.png: 核心逻辑伪代码/流程图
-  启动后端服务


> python app.py



启动前端界面
打开一个新的终端窗口，进入前端目录并运行：

> cd my-vue-app
> npm install
> npm run dev


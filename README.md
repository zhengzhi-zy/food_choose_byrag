# Food Choose by RAG / 食谱知识库 RAG 问答系统

[中文说明](#中文说明) | [English](#english)

## 中文说明

这是一个基于 LlamaIndex 的食谱 Markdown 文档垂直领域 RAG 问答系统。系统会加载本地食谱文档，构建 FAISS 向量索引，并结合 BM25、向量检索、RRF 重排、元数据过滤和查询路由，为用户提供菜品推荐、食材查询和分步骤做法说明。

本项目默认通过 OpenAI-compatible API 调用 DeepSeek，也可通过配置切换到其他 OpenAI-compatible 模型服务。API Key 只通过环境变量读取，不应写入代码或提交到 GitHub。

### 核心能力

- 加载 Markdown 食谱文档并增强元数据
- 按 Markdown 标题结构化分块
- 父子文档检索：子块负责精准召回，父文档负责完整回答
- LlamaIndex HuggingFace Embedding + FAISS 向量索引
- BM25 稀疏检索 + 向量检索混合召回
- RRF 融合重排
- 基于 `category` / `difficulty` 的元数据过滤
- 查询路由：`list` / `detail` / `general`
- 对模糊问题进行查询重写
- 支持流式和非流式回答
- DeepSeek / OpenAI-compatible 模型接口可配置

### 项目结构

```text
recipe_knowledge_rag/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
└── rag_modules/
    ├── __init__.py
    ├── data_preparation.py
    ├── index_construction.py
    ├── retrieval_optimization.py
    └── generation_integration.py
```

### 快速开始

1. 创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. 安装依赖：

```powershell
pip install -r requirements.txt
```

3. 配置 API Key：

```powershell
Copy-Item .env.example .env
```

然后编辑 `.env`：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

也可以直接在 PowerShell 中设置环境变量：

```powershell
$env:DEEPSEEK_API_KEY="your_api_key_here"
```

4. 准备食谱数据。

默认数据路径在 `config.py` 中：

```python
data_path = "../../data/C8/cook"
```

如果你的数据目录不同，请修改 `RAGConfig.data_path`。数据目录应包含 Markdown 格式的食谱文件。

5. 运行交互式问答：

```powershell
python main.py
```

### 配置说明

主要配置位于 `config.py` 的 `RAGConfig`：

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `data_path` | `../../data/C8/cook` | 食谱 Markdown 数据目录 |
| `index_save_path` | `./vector_index` | FAISS 索引保存目录 |
| `embedding_model` | `BAAI/bge-small-zh-v1.5` | HuggingFace 嵌入模型 |
| `llm_provider` | `deepseek` | 大模型服务商 |
| `llm_model` | `deepseek-chat` | 生成模型名称 |
| `llm_api_key_env` | `DEEPSEEK_API_KEY` | API Key 环境变量名 |
| `llm_base_url` | `https://api.deepseek.com/v1` | OpenAI-compatible 接口地址 |
| `top_k` | `3` | 检索返回数量 |
| `temperature` | `0.1` | 生成温度 |
| `max_tokens` | `2048` | 最大生成 token 数 |



## English

Food Choose by RAG is a LlamaIndex-based domain-specific RAG question-answering system for recipe Markdown documents. It loads local recipe files, builds a FAISS vector index, and combines BM25, vector retrieval, RRF reranking, metadata filtering, and query routing to answer recipe recommendation, ingredient, and step-by-step cooking questions.

The default LLM backend is DeepSeek through an OpenAI-compatible API. Other OpenAI-compatible model providers can also be configured. API keys are read from environment variables only and should never be committed to GitHub.

### Features

- Load Markdown recipe documents and enrich metadata
- Split documents by Markdown headers
- Parent-child document retrieval: child chunks for precise recall, parent documents for complete answers
- LlamaIndex HuggingFace Embeddings + FAISS vector index
- Hybrid retrieval with BM25 and vector search
- RRF reranking
- Metadata filtering by `category` and `difficulty`
- Query routing: `list`, `detail`, and `general`
- Query rewriting for ambiguous questions
- Streaming and non-streaming answers
- Configurable DeepSeek and OpenAI-compatible LLM backends

### Project Structure

```text
recipe_knowledge_rag/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
└── rag_modules/
    ├── __init__.py
    ├── data_preparation.py
    ├── index_construction.py
    ├── retrieval_optimization.py
    └── generation_integration.py
```

### Quick Start

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Configure your API key:

```powershell
Copy-Item .env.example .env
```

Then edit `.env`:

```env
DEEPSEEK_API_KEY=your_api_key_here
```

You can also set the variable directly in PowerShell:

```powershell
$env:DEEPSEEK_API_KEY="your_api_key_here"
```

4. Prepare recipe data.

The default data path is configured in `config.py`:

```python
data_path = "../../data/C8/cook"
```

If your data is stored elsewhere, update `RAGConfig.data_path`. The data directory should contain recipe files in Markdown format.

5. Run the interactive QA app:

```powershell
python main.py
```

### Configuration

Main configuration lives in `RAGConfig` inside `config.py`:

| Option | Default | Description |
| --- | --- | --- |
| `data_path` | `../../data/C8/cook` | Recipe Markdown data directory |
| `index_save_path` | `./vector_index` | FAISS index output directory |
| `embedding_model` | `BAAI/bge-small-zh-v1.5` | HuggingFace embedding model |
| `llm_provider` | `deepseek` | LLM provider |
| `llm_model` | `deepseek-chat` | Generation model name |
| `llm_api_key_env` | `DEEPSEEK_API_KEY` | API key environment variable name |
| `llm_base_url` | `https://api.deepseek.com/v1` | OpenAI-compatible API base URL |
| `top_k` | `3` | Number of retrieved results |
| `temperature` | `0.1` | Generation temperature |
| `max_tokens` | `2048` | Maximum generated tokens |



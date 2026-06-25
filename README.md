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

### 安全说明

- 不要把真实 API Key 写入代码、README 或提交历史。
- `.env`、`.venv`、`.idea`、`__pycache__` 和 `vector_index` 已在 `.gitignore` 中忽略。
- `.env.example` 只保留占位符，可安全提交。
- `vector_index` 是本地生成的索引目录，通常不需要上传到 GitHub。
- 迁移到 LlamaIndex 后，旧版生成的 `vector_index` 不再复用；首次运行会自动重建索引。

### 技术改写点

相较原始 Datawhale All-in-RAG C8 示例，本项目做了以下轻量改写：

1. 使用 LlamaIndex 重构 RAG 底层组件，包括 Document/Node、VectorStoreIndex、FAISS Vector Store、BM25 Retriever 和 OpenAI-compatible LLM。
2. 默认使用 `DeepSeek API + OpenAI-compatible` 调用方式。
3. 在配置层新增 `llm_provider`、`llm_api_key_env`、`llm_base_url`，便于切换不同模型服务商。
4. 保留数据准备、索引构建、检索优化、生成集成四层架构。
5. 保留父子文档、混合检索、RRF、Metadata Filter、查询路由和查询重写等核心 RAG 技术点。

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

### Security Notes

- Do not put real API keys in code, README files, or Git history.
- `.env`, `.venv`, `.idea`, `__pycache__`, and `vector_index` are ignored by `.gitignore`.
- `.env.example` contains placeholders only and is safe to commit.
- `vector_index` is generated locally and usually should not be uploaded to GitHub.
- After the LlamaIndex migration, the previously generated `vector_index` is not reused; the first run rebuilds the index automatically.

### Technical Notes

Compared with the original Datawhale All-in-RAG C8 example, this project adds a lightweight RAG and LLM integration rewrite:

1. LlamaIndex is used for the RAG foundation, including Document/Node, VectorStoreIndex, FAISS Vector Store, BM25 Retriever, and OpenAI-compatible LLM integration.
2. DeepSeek is used by default through an OpenAI-compatible API.
3. `llm_provider`, `llm_api_key_env`, and `llm_base_url` make provider switching easier.
4. The original four-layer RAG flow is preserved: data preparation, index construction, retrieval optimization, and generation integration.
5. Core RAG techniques are preserved, including parent-child retrieval, hybrid retrieval, RRF, metadata filters, query routing, and query rewriting.

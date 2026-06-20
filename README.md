# 食谱知识库 RAG 问答系统

这是一个面向食谱 Markdown 文档的垂直领域 RAG 问答系统。项目保留 Datawhale All-in-RAG C8 示例的核心架构，并做了轻量技术改写：将生成模块改为可配置的大模型接口，默认支持通过 OpenAI-compatible API 调用 DeepSeek，也保留 Moonshot/Kimi 接入方式。

## 核心能力

- Markdown 食谱文档加载与元数据增强
- 按 Markdown 标题进行结构化分块
- 父子文档检索：子块负责精准命中，父文档负责完整回答
- HuggingFace Embedding + FAISS 向量索引
- BM25 稀疏检索 + 向量检索混合召回
- RRF 融合重排
- 基于 `category` / `difficulty` 的 Metadata Filter
- 查询路由：`list` / `detail` / `general`
- 查询重写：对模糊问题补充检索语义
- Prompt 模板路由：列表推荐、分步骤做法、一般问答
- DeepSeek / Moonshot 等大模型接口可配置接入

## 项目结构

```text
recipe_knowledge_rag/
├── main.py
├── config.py
├── requirements.txt
└── rag_modules/
    ├── data_preparation.py
    ├── index_construction.py
    ├── retrieval_optimization.py
    └── generation_integration.py
```

## 运行方式

安装依赖：

```bash
pip install -r requirements.txt
```

配置 DeepSeek API Key：

```bash
set DEEPSEEK_API_KEY=your_api_key
```

如果使用 PowerShell：

```powershell
$env:DEEPSEEK_API_KEY="your_api_key"
```

运行交互式问答：

```bash
python main.py
```

默认数据路径在 `config.py` 中：

```python
data_path = "../../data/C8/cook"
```

如果本地数据目录不同，请修改 `RAGConfig.data_path`。

## 技术改写点

相较原 C8 示例，本项目主要做了轻量改写：

1. 将生成模块从固定 Moonshot/Kimi 接入，改为可配置的大模型接口。
2. 默认使用 `DeepSeek API + OpenAI-compatible` 调用方式。
3. 在配置层新增 `llm_provider`、`llm_api_key_env`、`llm_base_url`，便于切换不同模型服务商。
4. 保留原始 RAG 主流程：数据准备、索引构建、检索优化、生成集成四层架构。
5. 保留父子文档、混合检索、RRF、Metadata Filter、查询路由和查询重写等核心技术点，便于简历和面试讲解。


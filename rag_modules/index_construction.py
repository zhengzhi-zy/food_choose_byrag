"""
索引构建模块
"""

import logging
from pathlib import Path
from typing import List

import faiss
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.schema import TextNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore

logger = logging.getLogger(__name__)


class IndexConstructionModule:
    """索引构建模块 - 负责向量化和索引构建"""

    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5", index_save_path: str = "./vector_index"):
        """
        初始化索引构建模块

        Args:
            model_name: 嵌入模型名称
            index_save_path: 索引保存路径
        """
        self.model_name = model_name
        self.index_save_path = index_save_path
        self.embeddings = None
        self.vectorstore = None
        self.storage_context = None
        self.index = None
        self.setup_embeddings()

    def setup_embeddings(self):
        """初始化嵌入模型"""
        logger.info(f"正在初始化嵌入模型: {self.model_name}")

        self.embeddings = HuggingFaceEmbedding(
            model_name=self.model_name,
            device="cpu",
            normalize=True,
        )

        logger.info("嵌入模型初始化完成")

    def _embedding_dimension(self) -> int:
        """获取当前嵌入模型输出维度。"""
        sample_embedding = self.embeddings.get_text_embedding("维度探测")
        return len(sample_embedding)

    def build_vector_index(self, chunks: List[TextNode]) -> VectorStoreIndex:
        """
        构建向量索引

        Args:
            chunks: 文档块列表

        Returns:
            LlamaIndex向量索引对象
        """
        logger.info("正在构建FAISS向量索引...")

        if not chunks:
            raise ValueError("文档块列表不能为空")

        dimension = self._embedding_dimension()
        faiss_index = faiss.IndexFlatL2(dimension)
        self.vectorstore = FaissVectorStore(faiss_index=faiss_index)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vectorstore)
        self.index = VectorStoreIndex(
            nodes=chunks,
            storage_context=self.storage_context,
            embed_model=self.embeddings,
        )

        logger.info(f"向量索引构建完成，包含 {len(chunks)} 个向量")
        return self.index

    def add_documents(self, new_chunks: List[TextNode]):
        """
        向现有索引添加新文档

        Args:
            new_chunks: 新的文档块列表
        """
        if not self.index:
            raise ValueError("请先构建向量索引")

        logger.info(f"正在添加 {len(new_chunks)} 个新文档到索引...")
        self.index.insert_nodes(new_chunks)
        logger.info("新文档添加完成")

    def save_index(self):
        """
        保存向量索引到配置的路径
        """
        if not self.storage_context:
            raise ValueError("请先构建向量索引")

        Path(self.index_save_path).mkdir(parents=True, exist_ok=True)
        self.storage_context.persist(persist_dir=self.index_save_path)
        logger.info(f"向量索引已保存到: {self.index_save_path}")

    def load_index(self):
        """
        从配置的路径加载向量索引

        Returns:
            加载的向量索引对象，如果加载失败返回None
        """
        if not self.embeddings:
            self.setup_embeddings()

        index_path = Path(self.index_save_path)
        if not index_path.exists():
            logger.info(f"索引路径不存在: {self.index_save_path}，将构建新索引")
            return None

        try:
            self.vectorstore = FaissVectorStore.from_persist_dir(self.index_save_path)
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vectorstore,
                persist_dir=self.index_save_path,
            )
            self.index = load_index_from_storage(
                self.storage_context,
                embed_model=self.embeddings,
            )
            logger.info(f"向量索引已从 {self.index_save_path} 加载")
            return self.index
        except Exception as e:
            logger.warning(f"加载向量索引失败: {e}，将构建新索引")
            return None

    def similarity_search(self, query: str, k: int = 5) -> List[TextNode]:
        """
        相似度搜索

        Args:
            query: 查询文本
            k: 返回结果数量

        Returns:
            相似文档列表
        """
        if not self.index:
            raise ValueError("请先构建或加载向量索引")

        retriever = self.index.as_retriever(similarity_top_k=k)
        return [item.node for item in retriever.retrieve(query)]

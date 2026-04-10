"""
Neo4j图数据库连接
"""
from typing import Optional, List, Dict, Any
from neo4j import GraphDatabase


class Neo4jClient:
    """Neo4j图数据库客户端"""

    def __init__(self, url: str, user: str, password: str):
        self.driver = GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        """关闭"""
        self.driver.close()

    async def run(
        self,
        cypher: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """执行Cypher查询"""
        with self.driver.session() as session:
            result = session.run(cypher, parameters)
            return [dict(record) for record in result]

    def create_node(
        self,
        label: str,
        properties: Dict[str, Any]
    ) -> str:
        """创建节点"""
        cypher = f"CREATE (n:{label} $props) RETURN id(n) as id"
        with self.driver.session() as session:
            result = session.run(cypher, {"props": properties})
            return result.single()["id"]

    def create_relationship(
        self,
        from_id: Any,
        to_id: Any,
        rel_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """创建关系"""
        cypher = f"""
        MATCH (a), (b)
        WHERE id(a) = $from_id AND id(b) = $to_id
        CREATE (a)-[r:{rel_type} $props]->(b)
        RETURN r
        """
        with self.driver.session() as session:
            result = session.run(cypher, {
                "from_id": from_id,
                "to_id": to_id,
                "props": properties or {}
            })
            return result.single() is not None

    def find_related(
        self,
        node_id: Any,
        rel_type: Optional[str] = None,
        depth: int = 1
    ) -> List[Dict[str, Any]]:
        """查找关联节点"""
        rel_pattern = f"[r:{rel_type}*1..{depth}]" if rel_type else "[r*1..{depth}]"
        cypher = f"""
        MATCH (n)-{rel_pattern}-(related)
        WHERE id(n) = $node_id
        RETURN related, r
        """
        with self.driver.session() as session:
            result = session.run(cypher, {"node_id": node_id})
            return [dict(record) for record in result]


# 全局实例
_neo4j: Optional[Neo4jClient] = None


def init_neo4j(url: str, user: str, password: str) -> Neo4jClient:
    """初始化Neo4j"""
    global _neo4j
    _neo4j = Neo4jClient(url, user, password)
    return _neo4j


def get_neo4j() -> Neo4jClient:
    """获取Neo4j实例"""
    if _neo4j is None:
        raise RuntimeError("Neo4j not initialized")
    return _neo4j

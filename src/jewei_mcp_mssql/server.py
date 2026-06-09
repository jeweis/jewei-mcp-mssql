"""MSSQL MCP Server 主入口"""

import os

from mcp.server.fastmcp import FastMCP

from jewei_mcp_mssql.tools.execute import ExecuteSqlInput, execute_sql
from jewei_mcp_mssql.tools.schema import (
    DescribeTableInput,
    ListDatabasesInput,
    ListTablesInput,
    describe_table,
    list_databases,
    list_tables,
)

mcp = FastMCP("mssql_mcp")


@mcp.tool(
    name="mssql_execute_sql",
    annotations={
        "title": "执行 SQL 语句",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def tool_execute_sql(params: ExecuteSqlInput) -> str:
    """执行 SQL 语句。

    支持 SELECT 查询以及可选的 INSERT / UPDATE / DELETE / DDL 操作。
    写操作权限通过环境变量控制：
    - MSSQL_ALLOW_INSERT=true   启用 INSERT
    - MSSQL_ALLOW_UPDATE=true   启用 UPDATE
    - MSSQL_ALLOW_DELETE=true   启用 DELETE
    - MSSQL_ALLOW_DDL=true      启用 DDL（CREATE/DROP/ALTER/TRUNCATE）

    默认仅允许 SELECT，所有写操作均被拒绝。

    参数：
        params.sql: 要执行的 SQL 语句
        params.database: 可选，覆盖默认数据库
        params.max_rows: SELECT 最大返回行数，默认 100，最大 500
        params.response_format: 输出格式，markdown 或 json
    """
    return await execute_sql(params)


@mcp.tool(
    name="mssql_list_databases",
    annotations={
        "title": "列出数据库",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def tool_list_databases(params: ListDatabasesInput) -> str:
    """列出当前连接用户可访问的所有数据库。

    参数：
        params.response_format: 输出格式，markdown 或 json
    """
    return await list_databases(params)


@mcp.tool(
    name="mssql_list_tables",
    annotations={
        "title": "列出数据表",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def tool_list_tables(params: ListTablesInput) -> str:
    """列出指定数据库下的所有表。

    参数：
        params.database: 数据库名称，不填则使用默认库
        params.schema: Schema 名称，默认 dbo
        params.response_format: 输出格式，markdown 或 json
    """
    return await list_tables(params)


@mcp.tool(
    name="mssql_describe_table",
    annotations={
        "title": "描述表结构",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def tool_describe_table(params: DescribeTableInput) -> str:
    """获取指定表的列结构，包括列名、数据类型、最大长度、可空性和默认值。

    参数：
        params.table_name: 表名
        params.schema: Schema 名称，默认 dbo
        params.database: 数据库名称，不填则使用默认库
        params.response_format: 输出格式，markdown 或 json
    """
    return await describe_table(params)


def main():
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "streamable_http":
        port = int(os.getenv("MCP_PORT", "8000"))
        mcp.run(transport="streamable_http", port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()

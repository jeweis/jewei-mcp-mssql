"""mssql_list_databases / mssql_list_tables / mssql_describe_table 工具实现"""

import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from jewei_mcp_mssql.utils.connection import execute, handle_db_error


class ListDatabasesInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    response_format: str = Field(
        default="markdown",
        description="输出格式：markdown 或 json",
        pattern="^(markdown|json)$",
    )


class ListTablesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    table_schema: str = Field(
        default="dbo",
        description="Schema 名称",
    )
    response_format: str = Field(
        default="markdown",
        description="输出格式：markdown 或 json",
        pattern="^(markdown|json)$",
    )


class DescribeTableInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    table_name: str = Field(..., description="表名", min_length=1)
    table_schema: str = Field(default="dbo", description="Schema 名称")
    response_format: str = Field(
        default="markdown",
        description="输出格式：markdown 或 json",
        pattern="^(markdown|json)$",
    )


async def list_databases(params: ListDatabasesInput) -> str:
    sql = "SELECT name, state_desc, create_date FROM sys.databases ORDER BY name"
    try:
        rows = await execute(sql)
    except Exception as e:
        return handle_db_error(e)

    if params.response_format == "json":
        return json.dumps(rows, ensure_ascii=False, default=str)

    if not rows:
        return "未找到任何数据库"

    lines = ["| 数据库名 | 状态 | 创建时间 |", "| --- | --- | --- |"]
    for r in rows:
        lines.append(f"| {r['name']} | {r['state_desc']} | {r['create_date']} |")
    return "\n".join(lines)


async def list_tables(params: ListTablesInput) -> str:
    sql = """
        SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_SCHEMA, TABLE_NAME
    """
    try:
        rows = await execute(sql, params=(params.table_schema,))
    except Exception as e:
        return handle_db_error(e)

    if params.response_format == "json":
        return json.dumps(rows, ensure_ascii=False, default=str)

    if not rows:
        return f"Schema `{params.table_schema}` 下未找到任何表"

    lines = ["| Schema | 表名 | 类型 |", "| --- | --- | --- |"]
    for r in rows:
        lines.append(f"| {r['TABLE_SCHEMA']} | {r['TABLE_NAME']} | {r['TABLE_TYPE']} |")
    return f"共 {len(rows)} 张表\n\n" + "\n".join(lines)


async def describe_table(params: DescribeTableInput) -> str:
    sql = """
        SELECT
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            ORDINAL_POSITION
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = %s AND TABLE_SCHEMA = %s
        ORDER BY ORDINAL_POSITION
    """
    try:
        rows = await execute(sql, params=(params.table_name, params.table_schema))
    except Exception as e:
        return handle_db_error(e)

    if not rows:
        return f"表 `{params.table_schema}.{params.table_name}` 不存在或无列信息"

    if params.response_format == "json":
        return json.dumps(rows, ensure_ascii=False, default=str)

    lines: list[str] = [
        f"## {params.table_schema}.{params.table_name}",
        "",
        "| # | 列名 | 类型 | 最大长度 | 可空 | 默认值 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        max_len = str(r["CHARACTER_MAXIMUM_LENGTH"]) if r["CHARACTER_MAXIMUM_LENGTH"] else "-"
        default = str(r["COLUMN_DEFAULT"]) if r["COLUMN_DEFAULT"] else "-"
        lines.append(
            f"| {r['ORDINAL_POSITION']} | {r['COLUMN_NAME']} | {r['DATA_TYPE']} "
            f"| {max_len} | {r['IS_NULLABLE']} | {default} |"
        )
    return "\n".join(lines)

"""pytds 连接管理，用 run_in_executor 包装同步调用"""

import asyncio
import os
from functools import partial
from typing import Any

import pytds


def _get_conn_params(database: str | None = None) -> dict:
    return {
        "server": os.getenv("MSSQL_HOST", "localhost"),
        "port": int(os.getenv("MSSQL_PORT", "1433")),
        "database": database or os.getenv("MSSQL_DATABASE", "master"),
        "user": os.getenv("MSSQL_USERNAME", ""),
        "password": os.getenv("MSSQL_PASSWORD", ""),
        "as_dict": True,
    }


def _sync_execute(sql: str, params: Any, database: str | None) -> list[dict]:
    conn_params = _get_conn_params(database)
    with pytds.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if cur.description:
                return cur.fetchall()
            conn.commit()
            return [{"affected_rows": cur.rowcount}]


async def execute(sql: str, params: Any = None, database: str | None = None) -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(_sync_execute, sql, params, database))


def handle_db_error(e: Exception) -> str:
    if isinstance(e, pytds.exceptions.LoginError):
        return "错误：认证失败，请检查 MSSQL_USERNAME / MSSQL_PASSWORD"
    if isinstance(e, pytds.exceptions.DatabaseError):
        return f"错误：SQL 执行失败 — {e}"
    if isinstance(e, OSError):
        return "错误：无法连接到 SQL Server，请检查 MSSQL_HOST / MSSQL_PORT"
    return f"错误：{type(e).__name__}: {e}"

# jewei-mcp-mssql

Microsoft SQL Server MCP Server — 让 AI 助手能够查询和操作 SQL Server，**无需安装任何本地驱动**（纯 Python 实现）。

## 特性

- 无驱动：基于 `python-tds`，无需 ODBC 驱动或 FreeTDS
- 权限控制：INSERT / UPDATE / DELETE / DDL 各自独立开关，默认全只读
- 支持 stdio 和 Streamable HTTP 两种传输模式

## 快速开始

### Claude Code

在项目 `.mcp.json` 或全局配置中添加：

```json
{
  "mcpServers": {
    "mssql": {
      "type": "stdio",
      "command": "uvx",
      "args": ["jewei-mcp-mssql"],
      "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "1433",
        "DB_NAME": "master",
        "DB_USER": "sa",
        "DB_PASSWORD": "your_password"
      }
    }
  }
}
```

### Cursor

在 `~/.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "mssql": {
      "command": "uvx",
      "args": ["jewei-mcp-mssql"],
      "env": {
        "DB_HOST": "localhost",
        "DB_USER": "sa",
        "DB_PASSWORD": "your_password"
      }
    }
  }
}
```

### OpenCode

在 `~/.opencode/opencode.json` 中添加：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "mssql": {
      "type": "local",
      "command": ["uvx", "jewei-mcp-mssql"],
      "enabled": true,
      "environment": {
        "DB_HOST": "localhost",
        "DB_USER": "sa",
        "DB_PASSWORD": "your_password"
      }
    }
  }
}
```

### Claude Desktop

在 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "mssql": {
      "command": "uvx",
      "args": ["jewei-mcp-mssql"],
      "env": {
        "DB_HOST": "localhost",
        "DB_USER": "sa",
        "DB_PASSWORD": "your_password"
      }
    }
  }
}
```

## 环境变量

### 连接配置

| 变量 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `DB_HOST` | SQL Server 主机地址 | 是 | `localhost` |
| `DB_PORT` | SQL Server 端口 | 否 | `1433` |
| `DB_NAME` | 默认数据库 | 否 | `master` |
| `DB_USER` | 用户名 | 是 | - |
| `DB_PASSWORD` | 密码 | 是 | - |

### 权限控制

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DB_ALLOW_INSERT` | 是否允许 INSERT | `false` |
| `DB_ALLOW_UPDATE` | 是否允许 UPDATE | `false` |
| `DB_ALLOW_DELETE` | 是否允许 DELETE | `false` |
| `DB_ALLOW_DDL` | 是否允许 DDL（CREATE/DROP/ALTER/TRUNCATE） | `false` |

### 传输模式

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `MCP_TRANSPORT` | 传输模式：`stdio` 或 `streamable_http` | `stdio` |
| `MCP_PORT` | HTTP 模式端口 | `8000` |

## 可用工具

| 工具 | 说明 |
|------|------|
| `mssql_get_db_info` | 获取当前数据库基本信息（版本、服务器名、当前用户等） |
| `mssql_execute_sql` | 执行 SQL 语句（SELECT 始终允许，写操作受环境变量控制） |
| `mssql_list_tables` | 列出当前数据库下的所有表 |
| `mssql_describe_table` | 获取表的列结构（列名、类型、可空性等） |

## 提示示例

```
查一下当前连接的是哪个数据库，SQL Server 版本是多少
```

```
列出当前数据库里所有的表
```

```
描述一下 dbo.Orders 表的结构
```

```
查询 dbo.Orders 表中最近 10 条记录
```

```
统计 dbo.Orders 表中每个状态的订单数量，按数量降序排列
```

## License

MIT

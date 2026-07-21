# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

书签管理应用 — 当前处于规划/初始化阶段，尚未有实际代码。

## 规划的技术栈

- 前端：Next.js 14 + TypeScript + Tailwind CSS
- 后端：Next.js API Routes
- 数据库：Prisma + SQLite
- 部署：Vercel

## 规划的目录结构

```
src/
├── app/           # Next.js App Router 页面
│   ├── api/       # API 路由
│   ├── layout.tsx # 全局布局
│   └── page.tsx   # 首页
├── components/    # React 组件
│   ├── ui/        # 通用UI组件
│   └── features/  # 业务组件
├── lib/           # 工具函数和配置
├── prisma/        # 数据库 schema 和迁移
└── types/         # TypeScript 类型定义
```

## 编码规范

- 使用函数式组件 + React Hooks
- 组件文件使用 PascalCase 命名（如 `BookmarkCard.tsx`）
- 工具函数使用 camelCase 命名
- API 路由返回统一格式：`{ success: boolean, data?: any, error?: string }`
- 所有数据库操作通过 Prisma Client 执行
- SQLite 数据库文件在 `prisma/dev.db`，不要提交到 Git
- 环境变量在 `.env` 文件中，不要提交到 Git
- 所有新功能先创建 Git 分支再开发


## 外部参考文档

- 修改前端视觉、调颜色、调间距时 → 必读 `docs/brand-visual.md`
- 写产品文案、按钮文字、提示语时 → 必读 `docs/copywriting-style.md`
- 写 API 、定义返回格式时 → 必读 `docs/api-conventions.md`

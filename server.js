const express = require('express');

const app = express();
app.use(express.json());

// --------------- 内存存储 ---------------
let todos = [];
let nextId = 1;

// --------------- 路由 ---------------

// GET /todos — 获取所有事项（支持 ?completed=true/false 过滤）
app.get('/todos', (req, res) => {
  const { completed } = req.query;
  if (completed !== undefined) {
    const isCompleted = completed === 'true';
    return res.json(todos.filter(t => t.completed === isCompleted));
  }
  res.json(todos);
});

// POST /todos — 创建新事项
app.post('/todos', (req, res) => {
  const { title } = req.body;
  if (!title || typeof title !== 'string' || !title.trim()) {
    return res.status(400).json({ error: 'title 是必填字段，且不能为空字符串' });
  }

  const todo = {
    id: nextId++,
    title: title.trim(),
    completed: false,
    createdAt: new Date().toISOString(),
  };
  todos.push(todo);
  res.status(201).json(todo);
});

// --------------- 启动 ---------------
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ 待办事项 API 已启动：http://localhost:${PORT}`);
});

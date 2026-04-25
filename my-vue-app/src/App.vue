<template>
  <div class="app-container">
    <header class="top-nav">
      <div class="logo-area">
        <span class="logo-icon">🧠</span>
        <h1>文化资源编译引擎</h1>
      </div>
      <div class="nav-right">
        <span class="nav-tag">📚上海立信会计金融学院</span>
      </div>
    </header>

    <main class="dashboard-layout">
      
      <aside class="left-col">
        <div class="col-header">
          <h3><span class="icon">💠</span> 文化资源库 · 元素池</h3>
        </div>

        <div class="resource-card">
          <h4>🐉 中国神话库</h4>
          <div class="tags">
            <span class="tag active">盘古开天</span>
            <span class="tag">女娲补天</span>
            <span class="tag">嫦娥奔月</span>
            <span class="tag">精卫填海</span>
          </div>
        </div>

        <div class="resource-card">
          <h4>🎨 汉元素图案库</h4>
          <div class="tags">
            <span class="tag active">云纹</span>
            <span class="tag">水纹</span>
            <span class="tag">回字纹</span>
            <span class="tag">马面裙纹</span>
          </div>
        </div>

        <div class="resource-card">
          <h4>🏙️ 城市历史特色库</h4>
          <div class="tags">
            <span class="tag active">上海·石库门</span>
            <span class="tag">杭州·西湖</span>
            <span class="tag">西安·大唐</span>
            <span class="tag">北京·故宫</span>
          </div>
        </div>

        <div class="sidebar-footer">
          <p>➔ 元素自动关联，支持跨库组合</p>
        </div>
      </aside>

      <section class="mid-col">
        <div class="workflow-card input-card">
          <div class="card-title">
            <span class="icon">⌨️</span> 客户需求输入
          </div>
          <textarea 
            v-model="userQuery" 
            placeholder="示例：在上海石库门内举办一场以神话为背景的中秋亲子互动，预算约2万元..."
            :disabled="isCompiling"
          ></textarea>
          <button 
            class="run-btn" 
            @click="startCompilation" 
            :disabled="isCompiling || !userQuery"
          >
            {{ isCompiling ? '⚡ 正在跨库编译中...' : '🚀 启动智能编译' }}
          </button>
        </div>

        <div class="process-steps" :class="{ 'is-active': isCompiling || compiledResult }">
          <div class="step-card" :class="{ active: currentStep >= 1 }">
            <div class="step-icon">⚙️</div>
            <div class="step-content">
              <h4>① 需求解析 · 关键词提取</h4>
              <p>自然语言识别 ➔ 生成语义标签</p>
            </div>
          </div>
          <div class="step-card" :class="{ active: currentStep >= 2 }">
            <div class="step-icon">🔍</div>
            <div class="step-content">
              <h4>② 元素匹配 · 从资料库智能调取</h4>
              <p>神话库 + 图案库 + 城市库 同步检索</p>
            </div>
          </div>
          <div class="step-card" :class="{ active: currentStep >= 3 }">
            <div class="step-icon">🧩</div>
            <div class="step-content">
              <h4>③ 创意组合 · 编译活动模块</h4>
              <p>根据空间类型自动推荐模块化组件</p>
            </div>
          </div>
          <div class="step-card" :class="{ active: currentStep >= 4 }">
            <div class="step-icon">📄</div>
            <div class="step-content">
              <h4>④ 方案编译 · 输出完整交付物</h4>
              <p>结构化输出至右侧输出舱</p>
            </div>
          </div>
        </div>
      </section>

      <aside class="right-col" :class="{ 'is-expanded': isPanelExpanded }">
        <div class="col-header flex-between">
          <h3><span class="icon">📤</span> 智能输出</h3>
          <button class="expand-toggle-btn" @click="isPanelExpanded = !isPanelExpanded" title="扩展/收起视图">
            {{ isPanelExpanded ? '◧ 收起视图' : '◨ 扩展视图' }}
          </button>
        </div>

        <div class="output-container">
          <div v-if="!compiledResult && !isCompiling" class="empty-state">
            等待系统接收指令，生成完整方案包...
          </div>
          
          <div v-else-if="isCompiling" class="loading-state">
            <div class="loader"></div>
            <p>正在生成活动流程与物料清单...</p>
          </div>

          <div v-else class="result-wrapper">
            <div class="scrollable-content">
              <div 
                class="accordion-item" 
                v-for="item in dynamicAccordionItems" 
                :key="item.id"
                :class="{ expanded: activeTab === item.id }"
              >
                <div class="accordion-header" @click="toggleTab(item.id)">
                  <span class="acc-title">{{ item.title }}</span>
                  <span class="acc-arrow">▼</span>
                </div>
                <div class="accordion-body" v-show="activeTab === item.id">
                  <div class="markdown-body" v-html="item.content"></div>
                </div>
              </div>
            </div>
            
            <div class="sticky-footer">
              <button class="export-btn" @click="exportToMd">
                📥 智能输出
              </button>
            </div>
          </div>
        </div>
      </aside>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { marked } from 'marked'; 

const userQuery = ref('');
const isCompiling = ref(false);
const compiledResult = ref('');
const currentStep = ref(0);
const isPanelExpanded = ref(false);
const activeTab = ref<string | null>(null);

const toggleTab = (tabName: string) => {
  activeTab.value = activeTab.value === tabName ? null : tabName;
};

// ==================== 核心升级：动态 Markdown 智能切片 ====================
const dynamicAccordionItems = computed(() => {
  const raw = compiledResult.value;
  if (!raw) return [];

  const regex = /^(#{1,4})\s+(.*)$/gm;
  const parts = raw.split(regex);

  if (parts.length === 1) {
    return [{ id: 'sec-all', title: '📑 完整方案原文', content: marked.parse(raw) }];
  }

  const sections = [];
  
  if (parts[0].trim()) {
    sections.push({ id: 'sec-intro', title: '🎯 方案前言', content: marked.parse(parts[0]) });
  }

  for (let i = 1; i < parts.length; i += 3) {
    const title = parts[i+1].trim();
    const text = parts[i+2] || '';
    
    if (title || text.trim()) {
      sections.push({
        id: `sec-${i}`,
        title: `🔹 ${title}`,
        content: marked.parse(text) 
      });
    }
  }
  return sections;
});

watch(dynamicAccordionItems, (newItems) => {
  if (newItems.length > 0) {
    activeTab.value = newItems[0].id;
  }
});

// 模拟动画流转
const simulateSteps = async () => {
  for (let i = 1; i <= 4; i++) {
    currentStep.value = i;
    await new Promise(res => setTimeout(res, 800)); 
  }
};

const startCompilation = async () => {
  if (!userQuery.value) return;
  
  isCompiling.value = true;
  compiledResult.value = '';
  currentStep.value = 0;
  isPanelExpanded.value = true; 
  activeTab.value = null;

  const simPromise = simulateSteps();

  try {
    const response = await fetch('http://localhost:5000/api/compile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: userQuery.value })
    });

    const data = await response.json();
    await simPromise; 

    if (response.ok && data.status === 'success') {
      compiledResult.value = data.data;
    } else {
      alert('编译失败: ' + data.message);
    }
  } catch (error) {
    console.error('API Error:', error);
    alert('请求后端失败！请检查 Python Flask (5000端口) 是否运行正常。');
  } finally {
    isCompiling.value = false;
    currentStep.value = 4;
  }
};

const exportToMd = () => {
  const blob = new Blob([compiledResult.value], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `智能输出_文化方案_${new Date().getTime()}.md`;
  a.click();
  URL.revokeObjectURL(url);
};
</script>

<style scoped>
/* ====== 基础重置与全局 ====== */
.app-container {
  min-height: 100vh;
  background-color: #F0F4F8; 
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #333;
}

/* ====== 顶部导航 ====== */
.top-nav {
  display: flex; justify-content: space-between; align-items: center;
  background-color: #3B71E8; color: white; padding: 15px 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.logo-area { display: flex; align-items: center; gap: 10px; }
.logo-area h1 { margin: 0; font-size: 1.4rem; font-weight: 600; }
.nav-tag { background: rgba(255,255,255,0.2); padding: 5px 12px; border-radius: 20px; font-size: 0.9rem; }

/* ====== 三栏布局框架 ====== */
.dashboard-layout {
  display: flex; gap: 20px; padding: 20px 30px;
  max-width: 1600px; margin: 0 auto; align-items: flex-start;
}
.left-col { flex: 0 0 280px; }
.mid-col { flex: 1; min-width: 400px; transition: all 0.4s ease; }

.right-col {
  flex: 0 0 380px; 
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.right-col.is-expanded { flex: 0 0 650px; }

.col-header { margin-bottom: 15px; }
.col-header h3 { margin: 0; font-size: 1.1rem; color: #1E3A8A; font-weight: 600; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }

.expand-toggle-btn {
  background: white; border: 1px solid #BFDBFE; color: #3B82F6;
  padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; cursor: pointer;
  transition: all 0.2s;
}
.expand-toggle-btn:hover { background: #EFF6FF; border-color: #3B82F6; }

/* ====== 左侧：资源库卡片 ====== */
.resource-card { background: white; border-radius: 12px; padding: 18px; margin-bottom: 15px; border: 1px solid #E5E7EB; }
.resource-card h4 { margin: 0 0 12px 0; font-size: 1rem; color: #1F2937; }
.tags { display: flex; flex-wrap: wrap; gap: 8px; }
.tag { background: #F3F4F6; color: #4B5563; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; }
.tag.active { background: #EFF6FF; color: #3B82F6; border: 1px solid #BFDBFE; font-weight: 500; }
.sidebar-footer { font-size: 0.8rem; color: #6B7280; text-align: center; }

/* ====== 中间：工作流 ====== */
.workflow-card { background: white; border-radius: 12px; padding: 24px; border: 1px solid #E5E7EB; margin-bottom: 20px; }
.card-title { font-size: 1.1rem; font-weight: 600; color: #1E3A8A; margin-bottom: 15px; }

textarea {
  width: 100%; height: 120px; padding: 15px; border: 1px solid #DBEAFE;
  background-color: #F8FAFC; border-radius: 8px; resize: none; font-size: 0.95rem;
  box-sizing: border-box; margin-bottom: 15px;
}
textarea:focus { outline: none; border-color: #3B82F6; background: white; }

.run-btn {
  width: 100%; background-color: #3B82F6; color: white; border: none;
  padding: 12px; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.run-btn:hover:not(:disabled) { background-color: #2563EB; box-shadow: 0 4px 10px rgba(59,130,246,0.3); }
.run-btn:disabled { background-color: #9CA3AF; cursor: not-allowed; }

.step-card {
  display: flex; gap: 15px; background: white; border-radius: 12px; padding: 20px; margin-bottom: 15px;
  border: 1px solid #E5E7EB; opacity: 0.6; transition: all 0.3s;
}
.step-card.active { opacity: 1; border-color: #BFDBFE; box-shadow: 0 4px 12px rgba(59,130,246,0.08); }
.step-icon { font-size: 1.8rem; }
.step-content h4 { margin: 0 0 5px 0; color: #1F2937; }
.step-content p { margin: 0; font-size: 0.85rem; color: #6B7280; }

/* ====== 右侧：输出舱 ====== */
.output-container {
  background: white; border-radius: 12px; height: calc(100vh - 120px); 
  border: 1px solid #E5E7EB; display: flex; flex-direction: column; overflow: hidden;
}

.empty-state { padding: 40px 20px; text-align: center; color: #9CA3AF; font-size: 0.9rem; }
.loading-state { padding: 60px 20px; text-align: center; color: #3B82F6; }
.loader { border: 3px solid #E5E7EB; border-top: 3px solid #3B82F6; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto 15px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

/* ================= 修复滚动条与吸底按钮机制 ================= */
.result-wrapper {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden; /* 外层不滚动 */
}

/* 独立的内容滚动区，不再被挤压 */
.scrollable-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

/* 永远固定在底部的操作栏 */
.sticky-footer {
  padding: 15px 20px;
  background-color: #FAFAFA;
  border-top: 1px solid #E5E7EB;
}

/* ================= 折叠面板 (Accordion) ================= */
.accordion-item {
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  margin-bottom: 12px;
  overflow: hidden;
  background-color: white; /* 确保背景色清晰 */
}
.accordion-header {
  background-color: #F8FAFC;
  padding: 14px 16px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  user-select: none;
  transition: background-color 0.2s;
}
.accordion-header:hover { background-color: #F1F5F9; }
.accordion-item.expanded .accordion-header {
  background-color: #EFF6FF;
  border-bottom: 1px solid #E5E7EB;
}
.acc-title { font-weight: 600; color: #1E3A8A; font-size: 0.95rem; }
.acc-arrow { font-size: 0.8rem; color: #9CA3AF; transition: transform 0.3s; }
.accordion-item.expanded .acc-arrow { transform: rotate(180deg); color: #3B82F6; }

.accordion-body {
  padding: 16px;
  background-color: white;
  animation: slideDown 0.3s ease-out;
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

.export-btn {
  background-color: #3B82F6; color: white; border: none; padding: 14px;
  border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s;
  width: 100%; font-size: 1rem; letter-spacing: 1px;
}
.export-btn:hover { background-color: #2563EB; box-shadow: 0 4px 10px rgba(59,130,246,0.3); }

/* Markdown 原文样式优化 */
.markdown-body { font-size: 0.9rem; line-height: 1.6; color: #374151; }
.markdown-body :deep(h1), .markdown-body :deep(h2), .markdown-body :deep(h3) { color: #1E3A8A; margin-top: 10px; margin-bottom: 10px; font-size: 1.05rem; }
.markdown-body :deep(ul) { padding-left: 20px; margin-top: 5px; }
.markdown-body :deep(table) { width: 100%; border-collapse: collapse; margin: 10px 0; }
.markdown-body :deep(th), .markdown-body :deep(td) { border: 1px solid #E5E7EB; padding: 6px 10px; }
.markdown-body :deep(th) { background-color: #F8FAFC; color: #1F2937; }
</style>
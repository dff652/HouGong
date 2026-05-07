import { useEffect, useState } from 'react';
import { useStore, TAB_DEFS, startPolling, stopPolling, isEdict, isArchived, initTopology } from './store';
import EdictBoard from './components/EdictBoard';
import MonitorPanel from './components/MonitorPanel';
import OfficialPanel from './components/OfficialPanel';
import ModelConfig from './components/ModelConfig';
import SkillsConfig from './components/SkillsConfig';
import SessionsPanel from './components/SessionsPanel';
import MemorialPanel from './components/MemorialPanel';
import TemplatePanel from './components/TemplatePanel';
import MorningPanel from './components/MorningPanel';
import TaskModal from './components/TaskModal';
// ConfirmDialog is used inside TaskModal as needed
import Toaster from './components/Toaster';
import CourtCeremony from './components/CourtCeremony';

export default function App() {
  const [topoLoaded, setTopoLoaded] = useState(false);
  const activeTab = useStore((s) => s.activeTab);
  const setActiveTab = useStore((s) => s.setActiveTab);
  const liveStatus = useStore((s) => s.liveStatus);
  const countdown = useStore((s) => s.countdown);
  const loadAll = useStore((s) => s.loadAll);

  const theme = window.document.cookie.includes('edictTheme=hougong') ? 'hougong' : 'shengbu';
  const toggleTheme = () => {
    const newTheme = theme === 'shengbu' ? 'hougong' : 'shengbu';
    fetch('/api/switch-theme', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ theme: newTheme })
    }).finally(() => {
      document.cookie = `edictTheme=${newTheme}; path=/; max-age=31536000`;
      window.location.reload();
    });
  };

  useEffect(() => {
    initTopology().then(() => {
      setTopoLoaded(true);
      startPolling();
    });
    return () => stopPolling();
  }, []);

  if (!topoLoaded) {
    return <div className="min-h-screen bg-[#0d1117] flex items-center justify-center text-white/50 text-xl">正在铺设朝堂...</div>;
  }

  // Compute header chips
  const tasks = liveStatus?.tasks || [];
  const edicts = tasks.filter(isEdict);
  const activeEdicts = edicts.filter((t) => !isArchived(t));
  const sync = liveStatus?.syncStatus;
  const syncOk = sync?.ok;

  // Tab badge counts
  const tabBadge = (key: string): string => {
    if (key === 'edicts') return String(activeEdicts.length);
    if (key === 'sessions') return String(tasks.filter((t) => !isEdict(t)).length);
    if (key === 'memorials') return String(edicts.filter((t) => ['Done', 'Cancelled'].includes(t.state)).length);
    if (key === 'monitor') {
      const activeDepts = tasks.filter((t) => isEdict(t) && t.state === 'Doing').length;
      return activeDepts + '活跃';
    }
    return '';
  };

  return (
    <div className="wrap">
      {/* ── Header ── */}
      <div className="hdr">
        <div>
          <div className="logo">三省六部 · 总控台</div>
          <div className="sub-text">OpenClaw Sansheng-Liubu Dashboard</div>
        </div>
        <div className="hdr-r">
          <button className="btn-refresh" onClick={toggleTheme} style={{ marginRight: '1rem', background: '#3b82f6' }}>
            🎭 {theme === 'shengbu' ? '切至后宫模式' : '切至三省模式'}
          </button>
          <span className={`chip ${syncOk ? 'ok' : syncOk === false ? 'err' : ''}`}>
            {syncOk ? '✅ 同步正常' : syncOk === false ? '❌ 服务器未启动' : '⏳ 连接中…'}
          </span>
          <span className="chip">{activeEdicts.length} 道旨意</span>
          <button className="btn-refresh" onClick={() => loadAll()}>
            ⟳ 刷新
          </button>
          <span style={{ fontSize: 11, color: 'var(--muted)' }}>⟳ {countdown}s</span>
        </div>
      </div>

      {/* ── Tabs ── */}
      <div className="tabs">
        {TAB_DEFS.map((t) => (
          <div
            key={t.key}
            className={`tab ${activeTab === t.key ? 'active' : ''}`}
            onClick={() => setActiveTab(t.key)}
          >
            {t.icon} {t.label}
            {tabBadge(t.key) && <span className="tbadge">{tabBadge(t.key)}</span>}
          </div>
        ))}
      </div>

      {/* ── Panels ── */}
      {activeTab === 'edicts' && <EdictBoard />}
      {activeTab === 'monitor' && <MonitorPanel />}
      {activeTab === 'officials' && <OfficialPanel />}
      {activeTab === 'models' && <ModelConfig />}
      {activeTab === 'skills' && <SkillsConfig />}
      {activeTab === 'sessions' && <SessionsPanel />}
      {activeTab === 'memorials' && <MemorialPanel />}
      {activeTab === 'templates' && <TemplatePanel />}
      {activeTab === 'morning' && <MorningPanel />}

      {/* ── Overlays ── */}
      <TaskModal />
      <Toaster />
      <CourtCeremony />

      {/* 动态主题样式覆盖 */}
      {theme === 'hougong' && (
        <style dangerouslySetInnerHTML={{
          __html: `
          body { --bg: #2d0e0e; --panel: #3a1515; --panel2: #4a1f1f; --acc: #fcd34d; --border: #7f1d1d; --line: #7f1d1d; }
          .hdr { background: #450a0a; border-bottom-color: #7f1d1d; }
          .tab.active { background: #7f1d1d; color: #fcd34d; }
          .logo { color: #fcd34d; text-shadow: 0 0 10px rgba(252,211,77,0.3); }
          .btn-action, .btn-refresh { background: #7f1d1d; color: #fcd34d; border-color: #991b1b; }
          .btn-action:hover, .btn-refresh:hover { background: #991b1b; }
          .tbadge { background: #fcd34d; color: #450a0a; }
          .chip { background: #7f1d1d; border-color: #991b1b; color: #fbd38d; }
        ` }} />
      )}
    </div>
  );
}

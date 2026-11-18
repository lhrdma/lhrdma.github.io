(function () {
  const COLORS = {
    primary: '#163b65',
    success: '#087e91',
    muted: '#94a3b8',
    text: '#1e293b',
    linkLight: 'rgba(37, 99, 235, 0.35)',
  };

  const nodes = [
    {
      id: 'beijing',
      name: '北京',
      x: 25,
      y: 10,
      isKey: true,
      traffic: 85,
      location: '北京邮电大学',
    },
    {
      id: 'shenzhen',
      name: '深圳',
      x: 50,
      y: 90,
      isKey: true,
      traffic: 92,
      location: '香港中文大学（深圳）',
    },
    {
      id: 'jinan',
      name: '济南',
      x: 45,
      y: 35,
      isKey: true,
      traffic: 68,
      location: '济南超算',
      image: 'assets/prototype/jinan.jpeg',
    },
    {
      id: 'nanjing',
      name: '南京',
      x: 52,
      y: 60,
      isKey: false,
      traffic: 42,
      location: '南京未来网络研究院',
    },
    {
      id: 'qingdao',
      name: '青岛',
      x: 70,
      y: 35,
      isKey: false,
      traffic: 56,
      location: '崂山实验室',
    },
    { id: 'yantai', name: '烟台', x: 70, y: 22, isKey: false, traffic: 24, location: '烟台大学' },
    {
      id: 'weihai',
      name: '威海',
      x: 75,
      y: 18,
      isKey: false,
      traffic: 10,
      location: '哈工大（威海）',
    },
    {
      id: 'dongying',
      name: '东营',
      x: 62,
      y: 25,
      isKey: false,
      traffic: 12,
      location: '东营云计算中心',
    },
    {
      id: 'weifang',
      name: '潍坊',
      x: 62,
      y: 32,
      isKey: false,
      traffic: 20,
      location: '环渤海算力中心',
    },
    {
      id: 'rizhao',
      name: '日照',
      x: 70,
      y: 44,
      isKey: false,
      traffic: 13,
      location: '日照职业技术学院',
    },
    { id: 'linyi', name: '临沂', x: 64, y: 46, isKey: false, traffic: 17, location: '临沂大学' },
    {
      id: 'zibo',
      name: '淄博',
      x: 54,
      y: 32,
      isKey: false,
      traffic: 18,
      location: '淄博高新区数据中心',
    },
    {
      id: 'binzhou',
      name: '滨州',
      x: 58,
      y: 20,
      isKey: false,
      traffic: 10.5,
      location: '山东航空学院',
    },
    {
      id: 'dezhou',
      name: '德州',
      x: 44,
      y: 22,
      isKey: false,
      traffic: 11,
      location: '齐鲁工业大学德州研究院',
    },
    {
      id: 'liaocheng',
      name: '聊城',
      x: 35,
      y: 32,
      isKey: false,
      traffic: 9.5,
      location: '聊城大学',
    },
    {
      id: 'taian',
      name: '泰安',
      x: 50,
      y: 38,
      isKey: false,
      traffic: 14,
      location: '泰安云计算中心',
    },
    {
      id: 'jining',
      name: '济宁',
      x: 50,
      y: 42,
      isKey: false,
      traffic: 16,
      location: '鲁南超算中心',
    },
    {
      id: 'heze',
      name: '菏泽',
      x: 42,
      y: 49,
      isKey: false,
      traffic: 12.5,
      location: '齐鲁工业大学（菏泽校区）',
    },
    {
      id: 'zaozhuang',
      name: '枣庄',
      x: 50,
      y: 48,
      isKey: false,
      traffic: 15,
      location: '鲁南超算中心',
    },
  ];

  const links = [
    { from: 'beijing', to: 'jinan', bandwidth: 100, utilization: 68 },
    { from: 'jinan', to: 'nanjing', bandwidth: 100, utilization: 38 },
    { from: 'nanjing', to: 'shenzhen', bandwidth: 100, utilization: 75 },
    { from: 'jinan', to: 'qingdao', bandwidth: 200, utilization: 56 },
    { from: 'jinan', to: 'zibo', bandwidth: 100, utilization: 18 },
    { from: 'jinan', to: 'zaozhuang', bandwidth: 100, utilization: 15 },
    { from: 'jinan', to: 'dongying', bandwidth: 10, utilization: 12 },
    { from: 'jinan', to: 'weifang', bandwidth: 100, utilization: 20 },
    { from: 'jinan', to: 'jining', bandwidth: 100, utilization: 16 },
    { from: 'jinan', to: 'taian', bandwidth: 10, utilization: 14 },
    { from: 'jinan', to: 'dezhou', bandwidth: 10, utilization: 11 },
    { from: 'jinan', to: 'liaocheng', bandwidth: 10, utilization: 9.5 },
    { from: 'jinan', to: 'binzhou', bandwidth: 10, utilization: 10.5 },
    { from: 'jinan', to: 'heze', bandwidth: 100, utilization: 12.5 },
    { from: 'qingdao', to: 'yantai', bandwidth: 100, utilization: 24 },
    { from: 'qingdao', to: 'weihai', bandwidth: 100, utilization: 10 },
    { from: 'qingdao', to: 'rizhao', bandwidth: 100, utilization: 13 },
    { from: 'qingdao', to: 'linyi', bandwidth: 100, utilization: 17 },
  ];

  let selectedNodeId = 'jinan';
  let trafficData = [];
  let citySparkData = {};

  function getNode(id) {
    return nodes.find((n) => n.id === id);
  }

  function countConnections(nodeId) {
    return links.filter((l) => l.from === nodeId || l.to === nodeId).length;
  }

  function linkKey(from, to) {
    return `${from}-${to}`;
  }

  function getLinkColor(bw) {
    if (bw === 200) return COLORS.success;
    if (bw === 10) return COLORS.linkLight;
    return COLORS.primary;
  }

  function getLinkWidth(bw) {
    if (bw === 200) return 2.5;
    if (bw === 10) return 0.8;
    return 1.5;
  }

  function randomTraffic(base) {
    return Math.max(0, Math.min(100, base + (Math.random() - 0.5) * base * 0.3));
  }

  function initTrafficData() {
    const base = getNode(selectedNodeId).traffic;
    trafficData = Array.from({ length: 30 }, (_, i) => ({
      t: i,
      v: randomTraffic(base),
    }));
    nodes.forEach((node) => {
      citySparkData[node.id] = Array.from({ length: 12 }, () => randomTraffic(node.traffic));
    });
  }

  function renderTrafficChart() {
    const svg = document.getElementById('traffic-chart');
    if (!svg) return;
    const w = 260,
      h = 120,
      pad = { t: 10, r: 10, b: 20, l: 35 };
    const cw = w - pad.l - pad.r;
    const ch = h - pad.t - pad.b;
    const maxV = 100;

    const points = trafficData
      .map((d, i) => {
        const x = pad.l + (i / (trafficData.length - 1)) * cw;
        const y = pad.t + ch - (d.v / maxV) * ch;
        return `${x},${y}`;
      })
      .join(' ');

    svg.innerHTML = `
      ${[0, 25, 50, 75, 100]
        .map((v) => {
          const y = pad.t + ch - (v / maxV) * ch;
          return `<line x1="${pad.l}" y1="${y}" x2="${w - pad.r}" y2="${y}" stroke="#e2e8f0" stroke-dasharray="2,2"/>
                <text x="${pad.l - 5}" y="${y + 3}" fill="${COLORS.muted}" font-size="8" text-anchor="end">${v}</text>`;
        })
        .join('')}
      <polyline points="${points}" fill="none" stroke="${COLORS.success}" stroke-width="2"/>
      <text x="${pad.l - 20}" y="${h / 2}" fill="${COLORS.muted}" font-size="8" transform="rotate(-90,${pad.l - 20},${h / 2})">Gbps</text>
    `;
  }

  function renderSparkline(data, color) {
    const w = 80,
      h = 20;
    const max = Math.max(...data, 1);
    const pts = data.map((v, i) => `${(i / (data.length - 1)) * w},${h - (v / max) * h}`).join(' ');
    return `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none"><polyline points="${pts}" fill="none" stroke="${color}" stroke-width="1.5"/></svg>`;
  }

  function renderTop5() {
    const list = document.getElementById('top5-list');
    if (!list) return;
    const sorted = [...nodes].sort((a, b) => b.traffic - a.traffic).slice(0, 5);
    list.innerHTML = sorted
      .map(
        (node, i) => `
      <div class="proto-top5-item">
        <span class="proto-top5-rank">${i + 1}</span>
        <span class="proto-top5-name">${node.name}</span>
        <span class="proto-top5-spark">${renderSparkline(citySparkData[node.id] || [], COLORS.success)}</span>
        <span class="proto-top5-val">${node.traffic.toFixed(1)}G</span>
      </div>
    `,
      )
      .join('');
  }

  function renderTopology() {
    const svg = document.getElementById('topology-map');
    if (!svg) return;

    const linkEls = links
      .map((link) => {
        const from = getNode(link.from);
        const to = getNode(link.to);
        const color = getLinkColor(link.bandwidth);
        const width = getLinkWidth(link.bandwidth);
        return `<line x1="${from.x}%" y1="${from.y}%" x2="${to.x}%" y2="${to.y}%"
        stroke="${color}" stroke-width="${width}" opacity="0.7"/>`;
      })
      .join('');

    const nodeEls = nodes
      .map((node) => {
        const isSelected = node.id === selectedNodeId;
        const color = node.isKey ? COLORS.success : COLORS.primary;
        const r = node.isKey ? 1.8 : 1.2;
        const glow = isSelected ? 'stroke="#2563eb" stroke-width="0.6"' : '';
        return `
        <g class="proto-node" data-id="${node.id}" style="cursor:pointer">
          <circle cx="${node.x}%" cy="${node.y}%" r="${r + (isSelected ? 0.6 : 0)}" fill="none" stroke="${color}" stroke-width="0.3" opacity="0.4"/>
          <circle cx="${node.x}%" cy="${node.y}%" r="${r}" fill="${color}" ${glow}/>
          <text x="${node.x}%" y="${node.y + 4}%" fill="${COLORS.text}" font-size="2.2" text-anchor="middle" font-weight="${node.isKey ? 700 : 400}">${node.name}</text>
        </g>`;
      })
      .join('');

    svg.innerHTML = `
      <defs>
        <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#e2e8f0" stroke-width="0.5"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#grid)"/>
      ${linkEls}
      ${nodeEls}
    `;

    svg.querySelectorAll('.proto-node').forEach((el) => {
      el.addEventListener('click', () => {
        selectedNodeId = el.dataset.id;
        const picker = document.getElementById('node-picker');
        if (picker) picker.value = selectedNodeId;
        document.getElementById('current-node-badge').textContent = getNode(selectedNodeId).name;
        initTrafficData();
        renderTrafficChart();
        renderTopology();
        renderNodeDetail();
      });
    });
  }

  function renderNodeDetail() {
    const panel = document.getElementById('node-detail');
    if (!panel) return;
    const node = getNode(selectedNodeId);
    const conn = countConnections(node.id);
    panel.innerHTML = `
      <div class="proto-detail-row"><span class="proto-detail-label">节点名称</span><span class="proto-detail-value">${node.name}</span></div>
      <div class="proto-detail-row"><span class="proto-detail-label">所在位置</span><span class="proto-detail-value">${node.location || '-'}</span></div>
      <div class="proto-detail-row"><span class="proto-detail-label">节点类型</span><span class="proto-detail-value">${node.isKey ? '关键节点' : '普通节点'}</span></div>
      <div class="proto-detail-row"><span class="proto-detail-label">当前流量</span><span class="proto-detail-value">${node.traffic.toFixed(1)} Gbps</span></div>
      <div class="proto-detail-row"><span class="proto-detail-label">连接数</span><span class="proto-detail-value">${conn}</span></div>
      ${node.image ? `<img src="${node.image}" alt="${node.name}" class="proto-node-image">` : ''}
    `;
  }

  function init() {
    initTrafficData();
    renderTrafficChart();
    renderTop5();
    renderTopology();
    renderNodeDetail();

    const select = document.createElement('select');
    select.id = 'node-picker';
    select.setAttribute('aria-label', '选择拓扑节点');
    select.innerHTML = nodes
      .map((node) => `<option value="${node.id}">${node.name}</option>`)
      .join('');
    select.value = selectedNodeId;
    const label = document.createElement('label');
    label.htmlFor = 'node-picker';
    label.className = 'node-picker-label';
    label.append('选择节点 ', select);
    document.querySelector('.proto-map-wrap').append(label);
    select.addEventListener('change', () => {
      selectedNodeId = select.value;
      document.getElementById('current-node-badge').textContent = getNode(selectedNodeId).name;
      initTrafficData();
      renderTrafficChart();
      renderTopology();
      renderNodeDetail();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

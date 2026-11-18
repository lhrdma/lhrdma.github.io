"""Build the visual preview using the reference site's unchanged copy."""
from pathlib import Path
from shutil import copyfile
from bs4 import BeautifulSoup
from html import escape

root = Path(__file__).resolve().parent
source = root.parent / 'example-site'
soup = BeautifulSoup((source / 'index.html').read_text(encoding='utf-8'), 'html.parser')
(root / 'assets').mkdir(exist_ok=True)
for name in ['arch.png', 'topo.png']:
    copyfile(source / 'index_files' / name, root / 'assets' / name)
copyfile(source / 'NSFC.png', root / 'assets' / 'NSFC.png')
title = soup.title.get_text(strip=True)
subtitle = soup.select_one('.logo-subtext').get_text(strip=True)

def header(active):
    links = [('index.html', '项目概况'), ('news.html', '最新新闻'), ('team.html', '项目团队'), ('innovation.html', '创新成果'), ('materials.html', '资料汇编'), ('prototype.html', '原型系统')]
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if label == active else '')+f'>{label}</a>' for url, label in links)
    return f'''<a class="skip" href="#main">跳至正文</a><header class="masthead"><div class="wrap brand-row"><a class="brand" href="index.html"><img src="assets/NSFC.png" alt="国家自然科学基金委员会标志" width="62" height="62"><div><strong>{title}</strong><small>{subtitle}</small></div></a><div class="brand-note">NATIONAL KEY R&amp;D PROGRAM OF CHINA<br>YOUNG SCIENTIST PROJECT</div><button class="menu-toggle" aria-expanded="false" aria-controls="primary-navigation">菜单</button></div><div class="nav-row" id="primary-navigation"><nav class="wrap" aria-label="主导航">{nav}</nav></div></header>'''

footer_source = soup.select_one('footer')
footer_source.select_one('.footer-nav').decompose()
footer = '<footer><div class="wrap"><div class="footer-grid">'
for section in footer_source.select('.footer-section'):
    heading = section.find('h4')
    heading.name = 'h2'
    footer += '<section>' + str(heading)
    listing = section.find('ul')
    if listing:
        for a in listing.select('a[target="_blank"]'):
            a['rel'] = 'noopener noreferrer'
        footer += str(listing)
    else:
        footer += '<p>国家重点研发计划<br>「多模态网络与通信」重点专项<br>青年科学家项目</p>'
    footer += '</section>'
footer += f'</div><div class="copyright"><span>© 2024–2027 {title} 项目组</span><span>国家重点研发计划 · 青年科学家项目</span></div></div></footer>'

def document(content, active, scripts=''):
    return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{escape(subtitle)}"><title>{active} · {title}</title><link rel="icon" href="assets/NSFC.png"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="pages.css"><script src="main.js" defer></script>{scripts}</head><body>{header(active)}{content}{footer}</body></html>'

network = '''<div class="network"><svg viewBox="0 0 450 275" role="img" aria-labelledby="network-title"><title id="network-title">广域 RDMA 传输研究示意图</title><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#d5e0e9"/></pattern></defs><rect width="450" height="275" fill="url(#dots)"/><g stroke="#b0c4d6" stroke-width="1.3" fill="none"><path d="M65 142 165 60 285 76 392 147 275 226 165 214Z M65 142 165 214 285 76 M165 60 275 226 392 147 M65 142H392"/><path d="M165 60V214 M285 76 275 226" stroke-dasharray="4 5"/></g><path d="M65 142 165 60 285 76 392 147" stroke="#087e91" stroke-width="2.5" fill="none"/><g fill="white" stroke="#163b65" stroke-width="2"><circle cx="65" cy="142" r="11"/><circle cx="165" cy="60" r="9"/><circle cx="285" cy="76" r="11"/><circle cx="392" cy="147" r="11"/><circle cx="275" cy="226" r="9"/><circle cx="165" cy="214" r="8"/></g><g fill="#087e91"><circle cx="65" cy="142" r="4"/><circle cx="165" cy="60" r="3"/><circle cx="285" cy="76" r="4"/><circle cx="392" cy="147" r="4"/></g><g font-family="Microsoft YaHei, sans-serif" font-size="11" fill="#45617a"><text x="35" y="177">发送端</text><text x="138" y="35">协同控制</text><text x="258" y="50">拥塞感知</text><text x="371" y="182">接收端</text></g><rect x="163" y="122" width="127" height="37" fill="#f5f8fb" stroke="#b8cbdc"/><text x="226" y="146" fill="#163b65" text-anchor="middle" font-family="Georgia, serif" font-size="17" letter-spacing="3">WIDE-AREA</text></svg><div class="network-caption"><span>广域 RDMA 传输研究</span><span>RESEARCH OVERVIEW</span></div></div>'''
hero = f'''<section class="hero"><div class="wrap hero-inner"><div class="hero-copy"><div class="eyebrow">国家重点研发计划 · 青年科学家项目</div><h1><span>拥塞感知的广域 RDMA</span><span>传输控制技术研究</span></h1><p>{subtitle}</p><div class="hero-actions"><a class="primary" href="#background">了解项目 <span aria-hidden="true">↗</span></a><a class="text-link" href="news.html">最新新闻 <span aria-hidden="true">→</span></a></div></div>{network}</div><div class="wrap hero-meta"><span>牵头单位 / 北京邮电大学</span><span>参与单位 / 香港中文大学（深圳）</span><span>山东省计算中心（国家超级计算济南中心）</span></div></section>'''
ids = ['background', 'objectives', 'approach', 'outcomes']
english = ['BACKGROUND', 'OBJECTIVES', 'APPROACH', 'EXPECTED OUTCOMES']
headings = soup.select('#info .content-block')[0].find_all('h4')
sections = ''
sidebar = '<aside class="section-nav" aria-label="本页目录"><div class="label">项目概况 / OVERVIEW</div>'
for i, h in enumerate(headings):
    label = h.get_text(strip=True)
    sidebar += f'<a href="#{ids[i]}"><span>0{i+1}</span>{label}</a>'
    sections += f'<section class="article-section" id="{ids[i]}"><div class="section-heading"><span class="number">0{i+1}</span><h2>{label}</h2><small>{english[i]}</small></div>{h.find_next_sibling("p")}'
    if i in (2, 3):
        name, caption = ('arch.png', '图 01 / 项目技术架构') if i == 2 else ('topo.png', '图 02 / 网络拓扑与应用验证')
        width, height = (4202, 999) if i == 2 else (3886, 1792)
        sections += f'<figure class="figure"><a href="assets/{name}" target="_blank" rel="noopener" aria-label="查看{caption}原图"><img loading="lazy" src="assets/{name}" width="{width}" height="{height}" alt="{caption}"></a><figcaption>{caption} <span>· 点击查看原图</span></figcaption></figure>'
    sections += '</section>'
sidebar += '<a href="#milestones"><span>05</span>项目时间轴线</a><a class="news-entry" href="news.html">最新新闻 <span aria-hidden="true">↗</span></a></aside>'
sections += '<section class="article-section" id="milestones"><div class="section-heading"><span class="number">05</span><h2>项目时间轴线</h2><small>MILESTONES</small></div><div class="timeline">'
for item in soup.select('.timeline-item'):
    sections += f'<article class="milestone"><time>{item.select_one(".timeline-date").get_text(strip=True)}</time><h3>{item.h4.get_text(strip=True)}</h3></article>'
sections += '</div></section><div class="news-banner"><div><strong>最新新闻</strong><p>项目进展与学术交流</p></div><a href="news.html">查看最新新闻 <span aria-hidden="true">→</span></a></div>'
(root / 'index.html').write_text(document(f'<main id="main">{hero}<div class="wrap page-body">{sidebar}<div>{sections}</div></div></main>', '项目概况'), encoding='utf-8')

news = '<main class="wrap news-page" id="main"><div class="eyebrow">NEWS &amp; UPDATES</div><h1>最新新闻</h1>'
for card in soup.select('.news-card'):
    img = card.find('img')
    asset = source / 'index_files' / Path(img['src']).name
    # The saved reference has one missing image; omit it rather than substitute an unrelated photo.
    picture = ''
    if asset.exists():
        copyfile(asset, root / 'assets' / asset.name)
        picture = f'<img src="assets/{asset.name}" alt="{escape(img.get("alt", ""))}" loading="lazy">'
    news += f'<article class="news-item"><time>{card.select_one(".news-date").get_text(strip=True)}</time><h2>{card.select_one(".news-content").get_text(strip=True)}</h2>{picture}</article>'
news += '</main>'
(root / 'news.html').write_text(document(news, '最新新闻'), encoding='utf-8')


def page_heading(label, english, description):
    return f'<section class="page-intro"><div class="wrap"><div class="eyebrow">{english}</div><h1>{label}</h1><p>{description}</p></div></section>'


def section_heading(number, label, english):
    return f'<div class="section-heading"><span class="number">{number:02}</span><h2>{label}</h2><small>{english}</small></div>'


def page_layout(label, english, description, entries, sections):
    nav = f'<aside class="section-nav" aria-label="本页目录"><div class="label">{label} / CONTENTS</div>'
    for i, (anchor, name) in enumerate(entries, 1):
        nav += f'<a href="#{anchor}"><span>{i:02}</span>{name}</a>'
    nav += '</aside>'
    return f'<main id="main">{page_heading(label, english, description)}<div class="wrap page-body">{nav}<div class="page-articles">{sections}</div></div></main>'


def load_page(name):
    return BeautifulSoup((source / f'{name}.html').read_text(encoding='utf-8'), 'html.parser')


def localize(fragment, page):
    """Copy referenced images and normalize saved HTML for the shared layout."""
    for img in list(fragment.select('img')):
        path = source / img['src'].removeprefix('./')
        if not path.exists():
            img.decompose()
            continue
        destination = root / 'assets' / page
        destination.mkdir(exist_ok=True)
        copyfile(path, destination / path.name)
        img['src'] = f'assets/{page}/{path.name}'
        img['loading'] = 'lazy'
    for element in fragment.select('[style]'):
        del element['style']
    for anchor in fragment.select('a[target="_blank"]'):
        anchor['rel'] = 'noopener noreferrer'
    return fragment


# Team: preserve the complete biographies while giving units and people a common rhythm.
team = load_page('team')
team_sections = ''
for i, (anchor, label, english) in enumerate([('units', '承担单位', 'PARTICIPATING INSTITUTIONS'), ('personnel', '承研人员', 'RESEARCH TEAM')], 1):
    section = localize(team.select_one(f'#{anchor}'), 'team')
    section.select_one('.team-subsection-title').decompose()
    for heading in section.select('h4'):
        heading.name = 'h3' if 'team-unit-label' in heading.get('class', []) else 'h4'
    team_sections += f'<section class="article-section" id="{anchor}">{section_heading(i, label, english)}{section.decode_contents()}</section>'
description = team.select_one('main .content-block > p').get_text(' ', strip=True)
(root / 'team.html').write_text(document(page_layout('项目团队', 'RESEARCH TEAM', description, [('units', '承担单位'), ('personnel', '承研人员')], team_sections), '项目团队'), encoding='utf-8')

# Innovations remain a separate long-form page, grouped by the reference's four directions.
innovation = load_page('innovation')
entries = []
innovation_sections = ''
for i, section in enumerate(innovation.select('main > section'), 1):
    anchor = section['id']
    label = section.select_one('.innovation-category').get_text(strip=True)
    entries.append((anchor, label))
    innovation_sections += f'<section class="article-section" id="{anchor}">{section_heading(i, label, ["ARCHITECTURE", "DETECTION", "CONTROL", "APPLICATIONS"][i-1])}'
    for block in section.select('.content-block'):
        innovation_sections += f'<article class="innovation-entry">{block.decode_contents()}</article>'
    innovation_sections += '</section>'
(root / 'innovation.html').write_text(document(page_layout('创新成果', 'RESEARCH INNOVATIONS', '传输架构 / 拥塞检测 / 拥塞控制 / 应用示范', entries, innovation_sections), '创新成果'), encoding='utf-8')

# References: use only known metadata; missing authors/DOIs are never invented.
materials = load_page('materials')
entries = []
reference_sections = ''
reference_number = 0
for i, section in enumerate(materials.select('main > .page-section'), 1):
    anchor = section['id']
    label = section.h3.get_text(strip=True)
    entries.append((anchor, label))
    reference_sections += f'<section class="article-section" id="{anchor}">{section_heading(i, label, ["PUBLICATIONS", "PATENTS", "STANDARDS", "THESES"][i-1])}<ol class="references" start="{reference_number+1}">'
    for item in section.select('.paper-item, .highlight-card'):
        reference_number += 1
        item_title = item.select_one('.paper-title, .highlight-title').get_text(' ', strip=True)
        meta = item.select_one('.paper-venue, .highlight-meta').get_text(' ', strip=True)
        kind = item.select_one('.paper-label')
        kind = kind.get_text(' ', strip=True) if kind else '专利'
        href = item.get('href')
        heading = f'<a href="{escape(href, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(item_title)}</a>' if href else escape(item_title)
        # Thesis author precedes the title; publication venue follows it.
        citation = f'{escape(meta)}. {heading}. <span class="reference-meta">{kind}.</span>' if anchor == 'talent' else f'{heading}. <span class="reference-meta">{escape(meta)}.</span>'
        reference_sections += f'<li><span class="reference-number" aria-hidden="true">[{reference_number}]</span><div class="reference-text">{citation}</div></li>'
    reference_sections += '</ol></section>'
(root / 'materials.html').write_text(document(page_layout('资料汇编', 'PUBLICATIONS & RESOURCES', '论文 / 专利 / 标准 / 人才培养', entries, reference_sections), '资料汇编'), encoding='utf-8')

# Prototype: retain the existing topology and every result table in the shared page shell.
prototype = load_page('prototype')
prototype_sections = ''
for i, (selector, anchor, label, english) in enumerate([('#topology', 'topology', '系统拓扑', 'SYSTEM TOPOLOGY'), ('#results-slide', 'results', '测试结果', 'TEST RESULTS'), ('#app-verify-slide', 'app-verify', '应用验证', 'APPLICATION VALIDATION')], 1):
    section = localize(prototype.select_one(selector), 'prototype')
    if i == 1:
        body = section.select_one('.proto-dashboard')
        # Nested main landmarks in a saved page become a regular layout container.
        body.select_one('main').name = 'div'
        for svg in body.select('svg'):
            if svg.has_attr('viewbox'):
                svg['viewBox'] = svg['viewbox']
                del svg['viewbox']
        body.select_one('.proto-map-title').name = 'h3'
        for heading in body.select('.proto-panel h4'):
            heading.name = 'h3'
        prototype_sections += f'<section class="article-section prototype-section" id="{anchor}">{section_heading(i, label, english)}<p class="prototype-note">节点信息沿用参考站；流量图为交互示意，非实时监测数据。</p>{body}</section>'
    else:
        section.select_one('h3').decompose()
        content = section.select_one('.proto-results-body')
        for heading in content.select('.proto-app-label'):
            heading.name = 'h3'
        for heading in content.select('thead th'):
            heading['scope'] = 'colgroup' if heading.has_attr('colspan') else 'col'
        prototype_sections += f'<section class="article-section prototype-section" id="{anchor}">{section_heading(i, label, english)}{content.decode_contents()}</section>'
prototype_html = page_layout('原型系统', 'PROTOTYPE & VALIDATION', '系统拓扑 / 测试结果 / 应用验证', [('topology', '系统拓扑'), ('results', '测试结果'), ('app-verify', '应用验证')], prototype_sections)
(root / 'prototype.html').write_text(document(prototype_html, '原型系统', '<script src="prototype.js" defer></script>'), encoding='utf-8')

script = (source / 'prototype_files' / 'prototype.js.下载').read_text(encoding='utf-8')
script = script.replace("primary: '#2563eb'", "primary: '#163b65'").replace("success: '#10b981'", "success: '#087e91'")
script = script.replace(", image: 'fig/figure/beijing.png'", '').replace(", image: 'fig/figure/shenzhen.png'", '').replace("fig/figure/jinan.jpeg", 'assets/prototype/jinan.jpeg')
# Keep the map and chart renderers, using native anchor navigation and a static preview.
start = script.index('  function updateProtoLayoutMetrics()')
end = script.index('  function init()')
script = script[:start] + script[end:]
script = script.replace('    initSectionNav();\n    setInterval(tick, 3000);', '''    const select = document.createElement('select');
    select.id = 'node-picker';
    select.setAttribute('aria-label', '选择拓扑节点');
    select.innerHTML = nodes.map(node => `<option value="${node.id}">${node.name}</option>`).join('');
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
    });''')
script = script.replace("        selectedNodeId = el.dataset.id;", "        selectedNodeId = el.dataset.id;\n        const picker = document.getElementById('node-picker');\n        if (picker) picker.value = selectedNodeId;")
(root / 'prototype.js').write_text(script, encoding='utf-8')

# Use the same intro band and reading width on the news archive as the other inner pages.
news_document = BeautifulSoup((root / 'news.html').read_text(encoding='utf-8'), 'html.parser')
news_items = ''.join(str(item) for item in news_document.select('.news-item'))
news_content = f'<main id="main">{page_heading("最新新闻", "NEWS & UPDATES", "项目进展 / 学术交流")}<div class="wrap news-archive">{news_items}</div></main>'
(root / 'news.html').write_text(document(news_content, '最新新闻'), encoding='utf-8')

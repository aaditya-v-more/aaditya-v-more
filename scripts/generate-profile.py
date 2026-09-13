#!/usr/bin/env python3
"""Build self-contained, responsive SVG artwork for the GitHub profile.

Standard library only. Run from any directory. All displayed facts live in the
README; the drawings are conceptual illustrations, not product screenshots.
"""
from pathlib import Path
from html import escape
import math
import sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'showcase'
OUT.mkdir(parents=True, exist_ok=True)
PALETTES = {
    'dark': dict(bg='#0d121b', panel='#17202c', ink='#edf4ff', muted='#a2afc0', line='#303d4e', lime='#d3fa80', cyan='#76deed', orange='#ffad82', purple='#c1acff', grid='#1c2939'),
    'light': dict(bg='#f3f6fa', panel='#ffffff', ink='#17283d', muted='#52667d', line='#cad5e2', lime='#507800', cyan='#087c91', orange='#ad4b24', purple='#7555bd', grid='#e1e8f0'),
}

def text(x, y, value, size=20, fill=None, weight=400, family='sans', extra=''):
    return f'<text x="{x}" y="{y}" class="{family}" font-size="{size}" font-weight="{weight}" fill="{fill or P["ink"]}" {extra}>{escape(value)}</text>'

def rect(x, y, w, h, fill, radius=0, stroke='none', extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" {extra}/>'

def line(x1, y1, x2, y2, color=None, width=1, extra=''):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color or P["line"]}" stroke-width="{width}" {extra}/>'

def circle(x, y, r, fill, extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'

def path(d, color, width=2, extra=''):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def pill(x, y, value, color, width=None):
    w = width or len(value) * 9.3 + 30
    return rect(x, y, w, 32, P['panel'], 16, P['line']) + text(x+15, y+21, value, 14, color, 600, 'mono')

def arrow(x, y, color, size=24):
    return path(f'M{x} {y+size}L{x+size} {y}M{x+3} {y}H{x+size}V{y+size-3}', color, 3)

def begin(w, h, title, accent='lime'):
    c = P[accent]
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<defs>
  <radialGradient id="aura"><stop stop-color="{c}" stop-opacity=".12"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>
  <linearGradient id="signal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{P['lime']}"/><stop offset="1" stop-color="{P['cyan']}"/></linearGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{P['grid']}" stroke-width=".7"/></pattern>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="24"/></clipPath>
</defs>
<style>
.sans{{font-family:Arial,Helvetica,sans-serif}} .mono{{font-family:'Courier New',monospace}}
.pulse{{animation:pulse 4s ease-in-out infinite}} .flow{{stroke-dasharray:4 15;animation:flow 14s linear infinite}}
@keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}} @keyframes flow{{to{{stroke-dashoffset:-152}}}}
@media(prefers-reduced-motion:reduce){{.pulse,.flow{{animation:none}}}}
</style>
<g clip-path="url(#card)">
'''
    s += rect(0, 0, w, h, P['bg'])
    s += rect(0, 0, w, h, 'url(#grid)')
    s += f'<ellipse cx="{w*.8}" cy="{h*.42}" rx="{w*.43}" ry="{h*.9}" fill="url(#aura)"/>'
    return s

def end(w, h):
    return '</g>' + rect(.5, .5, w-1, h-1, 'none', 24, P['line']) + '</svg>\n'

def save(name, content):
    (OUT / name).write_text(content)

def torus(cx, cy, scale=1):
    def project(u, v):
        r = 103 + 39*math.cos(v)
        x, y, z = r*math.cos(u), r*math.sin(u), 39*math.sin(v)
        y, z = y*.67-z*.74, y*.74+z*.67
        x, y = x*.94-y*.342, x*.342+y*.94
        return cx+x*scale, cy+y*scale, z
    curves = []
    for i in range(34):
        pts = [project(i*2*math.pi/34, j*2*math.pi/80) for j in range(81)]
        curves.append((sum(q[2] for q in pts)/81, pts, False))
    for i in range(17):
        pts = [project(j*2*math.pi/140, i*2*math.pi/17) for j in range(141)]
        curves.append((sum(q[2] for q in pts)/141, pts, i==4))
    s = f'<ellipse cx="{cx}" cy="{cy+120*scale}" rx="{130*scale}" ry="{17*scale}" fill="{P["ink"]}" opacity=".035"/>'
    for depth, pts, lit in sorted(curves, key=lambda q:q[0]):
        d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x,y,z in pts)
        opacity = .2 + (depth+110)/220*.45
        s += path(d, 'url(#signal)', 1 if not lit else 2, f'opacity="{opacity:.2f}"')
        if lit: s += path(d, P['ink'], 2, 'class="flow" opacity=".8"')
    s += circle(cx+128*scale, cy-17*scale, 5, P['lime'], 'class="pulse"')
    return s

def hero(mobile):
    w,h = (640,740) if mobile else (1040,490)
    s = begin(w,h,'Aaditya More — software engineer. Developer tools, interactive learning and playable worlds.')
    s += circle(42,39,4,P['lime']) + text(55,44,'SOFTWARE ENGINEER',15,P['muted'],600,'mono', 'letter-spacing="2"')
    s += text(w-42,44,'AM / 01',14,P['muted'],400,'mono','text-anchor="end"')
    if mobile:
        s += text(37,151,'Aaditya',92,weight=800,extra='letter-spacing="-5"')
        s += text(37,243,'More',92,weight=800,extra='letter-spacing="-5"')
        s += circle(255,232,8,P['lime'])
        s += text(42,292,'Developer tools. Interactive learning.',23,P['muted'])
        s += text(42,325,'Playable worlds.',23,P['muted'])
        s += torus(320,505,1.12)
        s += text(42,683,'PYTHON  /  SWIFT  /  TYPESCRIPT',19,P['ink'],600,'mono')
        s += text(42,715,'DELL TECHNOLOGIES  ·  BENGALURU',15,P['muted'],400,'mono')
    else:
        s += text(39,170,'Aaditya',122,weight=800,extra='letter-spacing="-7"')
        s += text(39,289,'More',122,weight=800,extra='letter-spacing="-7"')
        s += circle(325,275,10,P['lime'])
        s += text(45,341,'Developer tools. Interactive learning.',24,P['muted'])
        s += text(45,375,'Playable worlds.',24,P['muted'])
        s += torus(796,237,1.22)
        s += text(796,421,'CURIOSITY → CODE → SOMETHING REAL',13,P['muted'],400,'mono','text-anchor="middle"')
        s += line(44,408,580,408)
        s += text(44,450,'PYTHON  /  SWIFT  /  TYPESCRIPT',18,P['ink'],600,'mono')
        s += text(44,474,'DELL TECHNOLOGIES  ·  BENGALURU',12,P['muted'],400,'mono')
    return s+end(w,h)

def window(x,y,w,h,name,color):
    s = rect(x,y,w,h,P['panel'],12,P['line'])
    s += circle(x+15,y+17,3,color) + text(x+28,y+21,name,12,P['muted'],600,'mono')
    s += line(x,y+34,x+w,y+34)
    return s

def graft_art():
    s = ''
    for x,y,name,c in [(5,0,'personal',P['orange']),(198,38,'work',P['purple'])]:
        s += window(x,y,176,130,name,c)
        s += rect(x+16,y+49,30,30,c,8)
        s += path(f'M{x+25} {y+64}h12M{x+31} {y+58}v12',P['bg'],2)
        s += rect(x+57,y+54,82,5,P['muted'],2)
        s += rect(x+57,y+69,60,4,P['line'],2)
        s += rect(x+16,y+95,105,5,P['line'],2)
        s += rect(x+16,y+107,133,5,P['line'],2)
    d = 'M93 130V157Q93 175 112 175H165Q188 175 188 193M286 168V175Q286 191 268 191H208Q188 191 188 203'
    s += path(d,P['line'],2)+path(d,P['orange'],2,'class="flow"')
    s += rect(75,202,227,44,P['panel'],10,P['orange'])
    s += text(188,230,'SHARED CODE HISTORY',13,P['orange'],600,'mono','text-anchor="middle"')
    return s

def ollama_art():
    s = window(0,8,386,223,'claude × ollama',P['cyan'])
    s += text(20,77,'> connect the dots_',22,P['ink'],600,'mono')
    for x,label in [(20,'CLAUDE'),(231,'OLLAMA')]:
        s += rect(x,101,134,58,P['bg'],9,P['line'])
        s += text(x+67,136,label,16,P['cyan'],600,'mono','text-anchor="middle"')
    s += path('M155 131H228',P['cyan'],2)+path('M155 131H228',P['ink'],3,'class="flow"')
    s += path('M219 125L228 131L219 137',P['cyan'],2)
    s += circle(24,192,4,P['cyan'],'class="pulse"')
    s += text(38,197,'CONTEXT · PACING · STREAMING',12,P['muted'],600,'mono')
    return s

def wqo_art():
    s = window(0,0,386,246,'research.workflow',P['purple'])
    d='M39 72V199'
    s += path(d,P['line'],2)+path(d,P['purple'],3,'class="flow"')
    for i,(label,detail) in enumerate([('Discover','datasets & fields'),('Simulate','expressions & backtests'),('Review','checks & audit trail'),('Submit','explicit approval')]):
        y=67+i*45
        s += circle(39,y,8,P['bg'],f'stroke="{P["purple"]}" stroke-width="2"')
        if i<3: s += circle(39,y,3,P['purple'])
        s += text(62,y+5,label,18,P['ink'],600)
        s += text(170,y+4,detail,12,P['muted'],400,'mono')
    return s

def router_art():
    s=rect(0,84,104,64,P['panel'],12,P['line'])+text(52,110,'ONE',13,P['muted'],600,'mono','text-anchor="middle"')+text(52,131,'SESSION',14,P['ink'],600,'mono','text-anchor="middle"')
    for i,(label,detail) in enumerate([('FAST','lower expected cost'),('BALANCED','cost × reliability'),('DEEP','higher capability')]):
        y=i*84
        d=f'M104 116H130Q155 116 155 {y+34}H190'
        s += path(d,P['line'],2)+path(d,P['lime'],2,'class="flow"')
        s += rect(190,y,197,67,P['panel'],10,P['line'])
        s += circle(206,y+21,3,P['lime'])+text(220,y+26,label,15,P['lime'],600,'mono')
        s += text(206,y+49,detail,11,P['muted'],400,'mono')
    return s

def play_art():
    def iso(x,y,z=0): return 191+(x-y)*24,51+(x+y)*12-z
    def poly(points,fill,stroke='none'):
        return f'<polygon points="{" ".join(f"{x},{y}" for x,y in points)}" fill="{fill}" stroke="{stroke}" stroke-width=".6"/>'
    def block(x,y,height,top,left,right):
        a,b,c,d=[iso(*p) for p in [(x,y),(x+1,y),(x+1,y+1),(x,y+1)]]
        aa,bb,cc,dd=[(xx,yy-height) for xx,yy in [a,b,c,d]]
        return poly([dd,cc,c,d],left)+poly([cc,bb,b,c],right)+poly([aa,bb,cc,dd],top)
    s=circle(325,29,22,P['orange'])
    s+=path('M20 189L192 278L373 185',P['line'],1)
    for y in range(7):
        for x in range(7):
            colors=('#314b49','#1c3539','#254041') if THEME=='dark' else ('#b9d7ca','#8fafac','#a1c7bd')
            s+=block(x,y,10,*colors)
            if x==3 or y==4: s+=poly([iso(x,y,10),iso(x+1,y,10),iso(x+1,y+1,10),iso(x,y+1,10)],'#ab9a77' if THEME=='light' else '#70785c')
    for x,y in [(1,1),(1,2),(5,1),(5,5),(1,5),(6,2)]:
        xx,yy=iso(x+.5,y+.5,10)
        s+=rect(xx-2,yy-28,4,30,'#8f7454')
        s+=poly([(xx,yy-61),(xx-16,yy-20),(xx+16,yy-20)],'#76b59b')
        s+=poly([(xx,yy-61),(xx,yy-20),(xx+16,yy-20)],'#3f8f75')
    for x,y in [(3,1),(4,1),(3,2),(4,2)]:
        s+=block(x,y,51,'#d8e3dc','#a0b4b4','#788e9d')
    for x,y in [(3,1),(4,1),(3,2),(4,2)]:
        xx,yy=iso(x+.5,y+.5,51)
        s+=poly([(xx,yy-36),(xx-24,yy),(xx,yy+12),(xx+24,yy)],'#d3fa80')
        s+=poly([(xx,yy-36),(xx,yy+12),(xx+24,yy)],'#90b764')
    xx,yy=iso(4,2,90)
    s+=line(xx,yy,xx,yy-42,P['muted'],2)+poly([(xx,yy-42),(xx+25,yy-34),(xx,yy-25)],P['orange'])
    return s

def learn_art():
    s=''
    layers=[[85,155,225],[55,100,145,190,235],[75,120,165,210],[105,175]]
    for li in range(3):
        for a in layers[li]:
            for b in layers[li+1]:
                s+=line(24+li*112,a,24+(li+1)*112,b,P['line'],1)
    s+=path('M24 155L136 100L248 165L360 105',P['cyan'],3,'class="flow"')
    for li,points in enumerate(layers):
        for ni,y in enumerate(points):
            c=P['cyan'] if (li+ni)%2 else P['purple']
            s+=circle(24+li*112,y,11,P['bg'],f'stroke="{c}" stroke-width="2"')
            s+=circle(24+li*112,y,4,c)
    s+=text(191,279,'TOKENS → ATTENTION → UNDERSTANDING',12,P['muted'],600,'mono','text-anchor="middle"')
    return s

PROJECTS=[
 dict(id='graft',title='Claude Graft',category='01 / NATIVE MACOS',lines=['One Mac.','More Claude.'],desc='Separate accounts. Shared context.',stack='SWIFT  /  SWIFTUI',accent='orange',art=graft_art),
 dict(id='ollama',title='Claude × Ollama',category='02 / DEVELOPER TOOLS',lines=['Your models.','Your workflow.'],desc='Claude Desktop, connected to Ollama.',stack='PYTHON  /  SHELL',accent='cyan',art=ollama_art),
 dict(id='wqo',title='WorldQuant Orchestrator',category='03 / RESEARCH AUTOMATION',lines=['From an idea','to a workflow.'],desc='Discover. Backtest. Review.',stack='PYTHON  /  SQLITE',accent='purple',art=wqo_art),
 dict(id='router',title='Devin Model Router',category='04 / MODEL ROUTING',lines=['One session.','The right route.'],desc='Route by expected cost and reliability.',stack='PYTHON  /  ACP',accent='lime',art=router_art),
 dict(id='play',title='Play — browser games by Aaditya More',category='SIDE QUEST / PLAY',lines=['Small worlds.','Big detours.'],desc='Strategy. Platforming. Endless running.',stack='OPEN A TAB. PLAY A LITTLE.',accent='orange',art=play_art),
 dict(id='learn',title='Learn — interactive textbook companions',category='DEEP DIVE / LEARN',lines=['Make the','theory click.'],desc='LLMs and deep learning, made interactive.',stack='READ  /  EXPERIMENT  /  UNDERSTAND',accent='cyan',art=learn_art),
]

def project(p,mobile):
    w,h=(640,650) if mobile else (1040,342)
    c=P[p['accent']]
    s=begin(w,h,p['title']+' — '+' '.join(p['lines']),p['accent'])
    s+=text(34,43,p['category'],15,c,600,'mono', 'letter-spacing="1"')
    s+=arrow(w-60,25,c,20)
    if mobile:
        for i,l in enumerate(p['lines']): s+=text(32,114+i*58,l,54,weight=700,extra='letter-spacing="-2"')
        s+=text(34,215,p['desc'],23,P['muted'])
        s+=f'<g transform="translate(112 265) scale(1.07)">{p["art"]()}</g>'
        s+=text(34,615,p['stack'],17,c,600,'mono')
    else:
        for i,l in enumerate(p['lines']): s+=text(33,120+i*62,l,58,weight=700,extra='letter-spacing="-2"')
        s+=text(36,229,p['desc'],21,P['muted'])
        s+=text(36,304,p['stack'],14,c,600,'mono')
        s+=f'<g transform="translate(592 62)">{p["art"]()}</g>'
    return s+end(w,h)

def footer(mobile):
    w,h=(640,205) if mobile else (1040,149)
    s=begin(w,h,'Explore all projects at aadityamore.com')
    s+=text(34,39,'THE REST OF MY INTERNET',13,P['muted'],600,'mono','letter-spacing="2"')
    s+=text(32,103 if mobile else 104,'aadityamore.com',45 if mobile else 59,weight=700,extra='letter-spacing="-2"')
    if mobile: s+=text(34,157,'PROJECTS  /  PLAY  /  LEARN  /  ABOUT',17,P['muted'],400,'mono')
    else: s+=text(669,91,'PROJECTS / PLAY / LEARN',14,P['muted'],400,'mono')
    s+=arrow(w-66,51 if not mobile else 82,P['lime'])
    return s+end(w,h)

def button(label,kind):
    w=156 if kind=='site' else 132
    bg='#d3fa80' if kind=='site' else '#182331'
    fg='#132119' if kind=='site' else '#e9f1fb'
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="44" viewBox="0 0 {w} 44" role="img"><title>{escape(label)}</title>'
    s+=rect(.5,.5,w-1,43,bg,10,'#344252')
    s+=f'<text x="17" y="28" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="600" fill="{fg}">{escape(label)}</text>'
    s+=arrow(w-29,16,fg,10)
    return s+'</svg>\n'

for THEME,P in PALETTES.items():
    for mobile in [False,True]:
        suffix=f'{"mobile-" if mobile else ""}{THEME}.svg'
        save('hero-'+suffix,hero(mobile))
        save('footer-'+suffix,footer(mobile))
        for p in PROJECTS: save(p['id']+'-'+suffix,project(p,mobile))
for label,kind in [('Portfolio','site'),('LinkedIn','linkedin'),('Résumé','resume')]: save('button-'+kind+'.svg',button(label,kind))
print(f'Generated {len(list(OUT.glob("*.svg")))} SVGs in {OUT}')

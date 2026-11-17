#!/usr/bin/env python3
"""Gera o site estático do Anderson (andersoncostaenf.com.br) em ./dist para GitHub Pages."""
import os, re, json, shutil, base64, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
DOMAIN = os.environ.get('SITE_DOMAIN', 'anerson.github.io')
BASE = f'https://{DOMAIN}'
HOJE = datetime.date.today().isoformat()
AUTOR = 'Anderson Costa'
CRED = 'Técnico de Enfermagem · COREN-SC 1418566'
IG = 'https://www.instagram.com/andersoncosta.enf/'

shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(DIST)

css = open(os.path.join(ROOT, 'base.css')).read()
css += """
/* páginas de guia */
.crumb{font:500 13px/1.4 var(--mono);color:var(--ink-2);padding-block:18px 0}
.crumb a{color:var(--ink-2)}
.art{max-width:760px;margin:0 auto;padding-block:28px 64px;display:grid;gap:22px}
.art h1{font-family:var(--sign);text-transform:uppercase;font-weight:800;font-size:clamp(40px,6vw,64px);line-height:.98}
.art h2{font-size:clamp(28px,4vw,38px);margin-top:18px}
.art p,.art li{font-size:19px;line-height:1.7}
.art ul,.art ol{margin:0;padding-left:1.2em;display:grid;gap:8px}
.art .resumo{border:2px solid var(--ink);border-radius:10px;padding:18px 20px;background:var(--sheet);display:grid;gap:8px}
.art .resumo .tag{color:var(--green)}
.author{display:grid;grid-template-columns:64px 1fr;gap:14px;align-items:center;padding:16px;border:1px solid var(--rule);border-radius:10px;background:var(--sheet)}
.author img{width:64px;height:64px;border-radius:50%;object-fit:cover;object-position:50% 30%}
.author b{display:block}
.author span{display:block;font:500 13px/1.4 var(--mono);color:var(--ink-2)}
.faq details{border-top:1px solid var(--rule);padding-block:12px}
.faq summary{cursor:pointer;font-weight:700;font-size:19px}
.faq p{margin-top:8px}
.mini{background:var(--mon);color:#DDE8E4}
.mini .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;padding-block:14px;font:500 13px/1.3 var(--mono)}
.mini a{color:var(--trace);text-decoration:none;font-weight:600}
.more{font:700 18px/1 var(--sign);letter-spacing:.06em;text-transform:uppercase;text-decoration:none}
"""
open(os.path.join(DIST, 'styles.css'), 'w').write(css)

# foto
src = open(os.path.join(ROOT, 'anderson-costa.html')).read()
m = re.search(r'data:image/jpeg;base64,([A-Za-z0-9+/=]+)', src)
open(os.path.join(DIST, 'foto.jpg'), 'wb').write(base64.b64decode(m.group(1)))

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'

def head(title, desc, path, jsonld):
    url = BASE + path
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{url}"><meta name="author" content="{AUTOR}">
<meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/foto.jpg"><meta property="og:locale" content="pt_BR">
<link rel="icon" href="/foto.jpg">{FONTS}<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script></head><body>"""

PERSON = {"@type": "Person", "name": "Anderson Adilson da Costa", "jobTitle": "Técnico de Enfermagem",
          "identifier": "COREN-SC 1418566", "url": BASE + "/", "sameAs": [IG],
          "alumniOf": {"@type": "CollegeOrUniversity", "name": "Unisociesc Blumenau"}}

FOOT = f"""<footer class="end"><div class="wrap"><div style="display:grid;gap:16px;align-content:start">
<span class="tag" style="color:var(--trace)">Fim do plantão</span><h2>Acompanhe no Instagram</h2>
<p>Vídeo novo toda semana. Parcerias e palestras: mensagem direta.</p>
<div class="ctas"><a class="btn on" href="{IG}" target="_blank" rel="noopener">@andersoncosta.enf</a></div></div>
<div class="alarm"><span class="tag">Emergência</span><b>Ligue 192</b><p>Conteúdo educativo. Não faço consulta nem orientação individual pela internet.</p></div></div>
<div class="wrap foot">{AUTOR} · {CRED} · Blumenau/SC</div></footer></body></html>"""

GUIAS = [
 dict(slug='como-evitar-queda-de-idoso-em-casa', titulo='Como evitar queda de idoso em casa: 4 coisas para tirar hoje',
  h1='Como evitar queda de idoso em casa', curto='Quedas em casa',
  desc='Tapete solto, fio no caminho, móvel baixo e escuro: o que tirar hoje da casa de um idoso para evitar quedas, explicado por um técnico de enfermagem, com fonte oficial.',
  resumo=['Tire tapetes soltos (no banheiro, só antiderrapante).', 'Prenda fios junto à parede.', 'Libere o caminho do quarto ao banheiro.', 'Deixe luz ao alcance da cama e luz de presença no corredor.', 'Instale barra de apoio perto do vaso e dentro do box.'],
  corpo="""<p>A maior parte das mudanças que deixam a casa de um idoso mais segura não custa nada. É tirar coisa do caminho. Antes de comprar qualquer equipamento, olhe o chão e o trajeto que a pessoa faz todo dia, principalmente do quarto ao banheiro, de madrugada.</p>
<h2>1. Tapete solto</h2><p>Tapete que escorrega ou dobra na ponta vira armadilha para quem arrasta um pouco os pés. Retire os tapetes soltos. No banheiro, use apenas o antiderrapante.</p>
<h2>2. Fio no caminho</h2><p>Fio de TV, telefone e extensão atravessando a passagem. Organize os fios junto à parede ou mude o aparelho de lugar para que nada cruze o caminho.</p>
<h2>3. Móvel baixo no meio da passagem</h2><p>Mesinha de centro, banquinho e pufe no trajeto são difíceis de enxergar, ainda mais à noite. Deixe o caminho livre.</p>
<h2>4. O escuro da madrugada</h2><p>Coloque um abajur ou interruptor ao alcance da cama e luzes de presença no corredor. Levantar no escuro para ir ao banheiro é um dos momentos de maior risco.</p>
<h2>O que vale colocar</h2><ul><li>Barras de apoio próximas ao vaso sanitário e dentro do box.</li><li>Sapato fechado, com sola antiderrapante e firme no calcanhar. Chinelo solto não segura o pé.</li></ul>
<h2>Se a pessoa cair</h2><p>Não puxe a pessoa pelos braços. Primeiro veja se há dor forte, deformidade, sangramento ou confusão. Se houver, não levante e ligue 192 (SAMU). Sem sinais de gravidade, a orientação é virar de lado, ficar de quatro apoios e subir apoiando-se em um móvel firme.</p>""",
  faq=[('Tapete antiderrapante resolve?', 'No banheiro, sim, ajuda. Tapete solto em outros cômodos continua sendo risco, mesmo com base emborrachada gasta.'),
       ('Onde instalar a barra de apoio?', 'Perto do vaso sanitário e dentro do box, que são os pontos de maior risco no banheiro.')],
  fontes=[('Cartilha de prevenção de quedas em idosos – Secretaria Municipal de Saúde de Santos (SP)', 'https://www.santos.sp.gov.br/static/files_www/files/portal_files/hotsites/idosoquedas/cartilhaprevencaoqueda_idosos.pdf')]),
 dict(slug='mudanca-de-decubito-acamado-de-quanto-em-quanto-tempo', titulo='Mudança de decúbito: de quanto em quanto tempo virar o paciente acamado',
  h1='De quanto em quanto tempo virar o paciente acamado', curto='Acamado e pele',
  desc='Mudança de posição a cada 2 horas, calcanhar sem apoio, pele limpa e hidratada e cabeceira até 30°: como prevenir lesão por pressão em casa, segundo o protocolo do Ministério da Saúde.',
  resumo=['O protocolo do Ministério da Saúde orienta reposicionar a cada 2 horas.', 'Calcanhares sem encostar no colchão: travesseiro sob a panturrilha.', 'Pele limpa, seca e hidratada.', 'Não massagear áreas avermelhadas ou ossos salientes.', 'Cabeceira até 30°, salvo orientação diferente da equipe.'],
  corpo="""<p>Colchão pneumático é um ótimo aliado, mas não faz o trabalho sozinho. Quem previne a ferida por pressão é a rotina de cuidado. Abaixo está o que o protocolo nacional orienta, em linguagem de casa. Siga sempre o que a equipe que acompanha a pessoa definir para o caso dela.</p>
<h2>A cada 2 horas</h2><p>O Protocolo para Prevenção de Úlcera por Pressão, do Ministério da Saúde, Anvisa e Fiocruz, orienta reposicionar o paciente a cada 2 horas. Uma tabela de horários na parede (08h, 10h, 12h…) ajuda a família a não esquecer e a revezar.</p>
<h2>Calcanhar no ar</h2><p>Os calcanhares devem ficar afastados da superfície da cama. Um travesseiro sob a panturrilha resolve: o pé fica "flutuando".</p>
<h2>Pele limpa, seca e hidratada</h2><p>Limpe sempre que sujar, com água morna e sabão neutro. Use hidratante na pele seca pelo menos uma vez ao dia, de preferência após o banho. Umidade de fralda e suor deixa a pele mais frágil.</p>
<h2>Não massageie a área vermelha</h2><p>Massagear ossos salientes ou pele avermelhada não previne a ferida. O protocolo orienta não fazer.</p>
<h2>Cabeceira até 30°</h2><p>Elevar mais que isso faz o corpo escorregar e arrastar a pele. Existem exceções (por exemplo, por indicação médica), por isso siga a orientação da equipe.</p>""",
  faq=[('Com colchão pneumático ainda precisa virar?', 'Sim. O colchão ajuda a redistribuir a pressão, mas a mudança de posição continua sendo orientada.'),
       ('A pele ficou vermelha. E agora?', 'Não massageie, alivie a pressão daquele ponto e avise a equipe de saúde que acompanha a pessoa.')],
  fontes=[('Protocolo para Prevenção de Úlcera por Pressão – Ministério da Saúde, Anvisa e Fiocruz (2013)', 'https://goias.gov.br/saude/wp-content/uploads/sites/34/2015/02/protocolo-para-prevencao-de-ulcera-por-pressao-17f.pdf')]),
 dict(slug='idoso-no-calor-sinais-de-desidratacao', titulo='Idoso no calor: sinais de desidratação e quando procurar ajuda',
  h1='Idoso no calor: sinais de desidratação', curto='Calor e idoso',
  desc='Com a idade a sede diminui. Como oferecer líquido ao idoso no calor, horários para evitar o sol e os sinais de alerta de desidratação, segundo nota técnica do Ministério da Saúde.',
  resumo=['Ofereça líquido antes da sede, mais que o habitual.', 'Evite álcool e cafeína nos dias de calor intenso.', 'Evite sol e atividade física das 10h às 15h.', 'Confusão mental, desmaio ou convulsão: ligue 192.'],
  corpo="""<p>Com a idade, a sensação de sede diminui. Muito idoso passa o dia inteiro sem pedir água, e no calor isso vira risco. Quem cuida precisa oferecer, não esperar o pedido.</p>
<h2>Ofereça antes da sede</h2><p>A nota técnica do Ministério da Saúde sobre onda de calor orienta oferecer mais líquido que o habitual, mesmo sem vontade de beber. Deixe um copo sempre à vista e ofereça ao longo do dia.</p>
<h2>Menos café e álcool</h2><p>Nos dias de calor intenso, a orientação é evitar bebida alcoólica e cafeína.</p>
<h2>Fuja do sol das 10h às 15h</h2><p>Atividade física e exposição ao sol, fora desse horário. Roupa leve e larga.</p>
<h2>Sinais de alerta</h2><ul><li>Sede excessiva, boca seca e saliva grossa.</li><li>Pele fria, pálida e pegajosa, cãibras.</li><li>Tontura, dor de cabeça, náusea, cansaço fora do normal.</li></ul>
<h2>Quando é urgência</h2><p>Confusão mental, desmaio ou convulsão: ligue 192 (SAMU). Se os sinais de desidratação não melhoram com a hidratação, procure atendimento.</p>""",
  faq=[('Quanto de água o idoso deve beber?', 'Depende da pessoa e de doenças como insuficiência cardíaca ou renal, que podem limitar líquidos. Confirme a quantidade com quem acompanha a saúde dele.'),
       ('Suco e chá contam?', 'Contam como líquido. Prefira opções sem cafeína e sem excesso de açúcar.')],
  fontes=[('Nota técnica conjunta sobre onda de calor – Ministério da Saúde (2023)', 'https://www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/notas-tecnicas/2023/nota-tecnica-conjunta-onda-calor.pdf')]),
]

AUTHOR_BOX = f"""<div class="author"><img src="/foto.jpg" alt="Anderson Costa" width="64" height="64"><div><b>Por {AUTOR}</b><span>{CRED}</span><span>Bacharel em Enfermagem · Unisociesc 2026</span></div></div>"""

for g in GUIAS:
    path = f"/guias/{g['slug']}/"
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": g['titulo'], "description": g['desc'], "inLanguage": "pt-BR",
         "datePublished": HOJE, "dateModified": HOJE, "author": PERSON, "mainEntityOfPage": BASE + path,
         "image": BASE + "/foto.jpg", "citation": [f[1] for f in g['fontes']]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g['faq']]}]}
    resumo = ''.join(f'<li>{r}</li>' for r in g['resumo'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in g['faq'])
    fontes = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in g['fontes'])
    outros = ''.join(f'<li><a href="/guias/{o["slug"]}/">{o["h1"]}</a></li>' for o in GUIAS if o is not g)
    html = head(g['titulo'] + ' | Anderson Costa', g['desc'], path, jsonld) + f"""
<header class="mini"><div class="wrap"><span>ANDERSON COSTA · {CRED.upper()}</span><a href="/">← Início</a></div></header>
<main class="wrap"><div class="crumb"><a href="/">Início</a> / <a href="/#prescricao">Guias</a> / {g['curto']}</div>
<article class="art">
<span class="tag" style="color:var(--green)">Guia · {g['curto']}</span>
<h1>{g['h1']}</h1>
{AUTHOR_BOX}
<div class="resumo"><span class="tag">Resumo rápido</span><ul>{resumo}</ul></div>
{g['corpo']}
<h2>Perguntas frequentes</h2><div class="faq">{faq}</div>
<h2>Fontes</h2><ul>{fontes}</ul>
<p class="note">Conteúdo educativo. Não substitui a avaliação da equipe de saúde que acompanha a pessoa. Em emergência, ligue 192.</p>
<h2>Leia também</h2><ul>{outros}</ul>
</article></main>""" + FOOT
    os.makedirs(DIST + path, exist_ok=True)
    open(DIST + path + 'index.html', 'w').write(html)

# página inicial: corpo da versão publicada, com links para os guias completos
body = src[src.index('</style>') + 8:]
body = body[body.index('<header class="monitor">'):]
body = re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', '/foto.jpg', body)
for sid, g in zip(['acamado', 'quedas', 'calor'], [GUIAS[1], GUIAS[0], GUIAS[2]]):
    marker = f'<article class="sheet" id="{sid}">'
    i = body.index(marker); j = body.index('</article>', i)
    body = body[:j] + f'<div class="sheet-b" style="padding-top:0"><a class="more" href="/guias/{g["slug"]}/">Ler o guia completo →</a></div>' + body[j:]
home_ld = {"@context": "https://schema.org", "@graph": [dict(PERSON, **{"@id": BASE + "/#anderson"}),
           {"@type": "WebSite", "name": "Anderson Costa Enfermagem", "url": BASE + "/", "inLanguage": "pt-BR"}]}
home = head('Anderson Costa | Técnico de Enfermagem · COREN-SC 1418566',
            'O que acontece no hospital, explicado por quem cuida. Guias práticos com fonte oficial para quem cuida de idoso e acamado em casa.', '/', home_ld)
home = home.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
open(os.path.join(DIST, 'index.html'), 'w').write(home + body + '</body></html>')

# =================================================================
# /casa-segura/ - vitrine de afiliados
# Colar em _fonte/build.py ANTES da linha "# 404, robots, sitemap, CNAME".
# Usa head(), FOOT, AUTHOR_BOX e PERSON que ja existem no arquivo.
# Item sem link de afiliado nao entra na pagina.
# Para o sitemap, trocar a linha das urls por:
#   urls = ['/'] + [f"/guias/{g['slug']}/" for g in GUIAS] + ['/casa-segura/']
# =================================================================

# ---------------------------------------------------------------- produtos
# Cole aqui o link de afiliado do Omron HEM-7156T.
# Vazio = o aparelho, a pergunta do pulso e a linha do resumo saem da pagina.
LINK_PRESSAO = ""

# Só itens com link de afiliado. Item sem link não entra na página.
COMODOS = [
 ("Banheiro", "O banheiro concentra o maior risco: piso molhado, pouco espaço para se apoiar e o trajeto da madrugada.", [
   dict(nome="Barra de apoio",
        modelo="Kit 4 barras de apoio em aço inox, 40 cm",
        porque="Perto do vaso e dentro do box, para ter onde segurar ao sentar e ao levantar.",
        conferir="Fixação com parafuso e bucha na parede (ventosa não serve), aço inox e a carga máxima informada na embalagem.",
        link="https://meli.la/1rdR6W3"),
   dict(nome="Tapete de borracha com ventosas",
        modelo="Tapete de PVC com ventosas, 63 x 35 cm",
        porque="Dentro do box, onde o piso fica molhado e escorregadio.",
        conferir="Ventosas em toda a base e tamanho que cubra a área onde a pessoa pisa.",
        link="https://meli.la/1Q41nwv"),
   dict(nome="Tapete antiderrapante para o piso",
        modelo="Tapete vazado antiderrapante Espumaço, 1,00 x 1,20 m",
        porque="Fora do box, na saída do banho, onde a água pinga.",
        conferir="Base que não escorrega e bordas baixas, para o tapete não virar tropeço.",
        link="https://meli.la/2ovCFmu"),
   dict(nome="Cadeira de banho",
        modelo="Dellamed D30, dobrável, até 100 kg",
        porque="Para quem fica instável em pé durante o banho.",
        conferir="Rodas com trava e a carga máxima suportada. Trave as rodas antes de a pessoa sentar ou levantar.",
        link="https://meli.la/25AJNKx"),
 ]),
 ("Saúde no dia a dia", ("Para acompanhar a saúde e para chamar ajuda." if LINK_PRESSAO else "Para a hora em que a pessoa precisa chamar alguém."), [
   dict(nome="Aparelho de pressão digital de braço",
        modelo="Omron HEM-7156T, de braço, com estudo de validação clínica publicado",
        porque="Para medir a pressão em casa e levar os valores anotados para a consulta.",
        conferir="Modelo de braço, não de pulso, com validação clínica, e manguito do tamanho do braço. Calibre uma vez por ano em local indicado pelo Inmetro.",
        link=LINK_PRESSAO),
   dict(nome="Campainha sem fio para pedir ajuda",
        modelo="Intelbras CIB 101, alcance de até 100 m",
        porque="Para chamar alguém da casa depois de uma queda ou de um mal-estar.",
        conferir="Alcance entre os cômodos da casa e botão que a pessoa consiga apertar sozinha.",
        link="https://meli.la/2EmobnM"),
 ]),
]

RESUMO = ([
 "Antes de comprar, tire o que atrapalha: tapete solto, fio no caminho, móvel baixo na passagem.",
 "Barra de apoio é o item de maior efeito no banheiro: perto do vaso e dentro do box.",
 "Nada aqui substitui a avaliação da equipe de saúde que acompanha a pessoa.",
] + (["Aparelho de pressão: de braço e com validação clínica, nunca de pulso."] if LINK_PRESSAO else []))

FAQ = ([
 ("Preciso comprar tudo isso?",
  "Não. A maior parte das mudanças que deixam a casa mais segura não custa nada: tirar tapete solto, prender fio junto à parede e liberar o caminho do quarto ao banheiro. Equipamento vem depois disso."),
 ("Barra de apoio com ventosa serve?",
  "Para sustentar o peso de uma pessoa, não. A fixação precisa ser com parafuso e bucha na parede, e a carga máxima vem informada na embalagem."),
 ("Andador ou bengala, qual escolher?",
  "Essa escolha depende de avaliação presencial, porque a altura e o tipo mudam conforme a pessoa. Por isso não indico modelo aqui."),
] + ([("Pode medir a pressão no pulso?",
  "A orientação das Diretrizes Brasileiras de Medidas da Pressão Arterial é usar aparelho de braço, automático e validado. Modelos de pulso não são indicados para acompanhamento em casa.")] if LINK_PRESSAO else []))

FONTES = [
 ("Cartilha de prevenção de quedas em idosos – Secretaria Municipal de Saúde de Santos (SP)",
  "https://www.santos.sp.gov.br/static/files_www/files/portal_files/hotsites/idosoquedas/cartilhaprevencaoqueda_idosos.pdf"),
 ("Protocolo para Prevenção de Úlcera por Pressão – Ministério da Saúde, Anvisa e Fiocruz (2013)",
  "https://goias.gov.br/saude/wp-content/uploads/sites/34/2015/02/protocolo-para-prevencao-de-ulcera-por-pressao-17f.pdf"),
]

GUIAS_LINKS = [
 ("Como evitar queda de idoso em casa", "/guias/como-evitar-queda-de-idoso-em-casa/"),
 ("De quanto em quanto tempo virar o paciente acamado", "/guias/mudanca-de-decubito-acamado-de-quanto-em-quanto-tempo/"),
 ("Idoso no calor: sinais de desidratação", "/guias/idoso-no-calor-sinais-de-desidratacao/"),
]
print("dados ok:", sum(len(c[2]) for c in COMODOS), "produtos")

# ---------------------------------------------------------------- página
PATH = '/casa-segura/'
TITULO = 'Casa segura para o idoso: o que eu indico e o que conferir antes de comprar'
DESC = ('Barra de apoio, tapete antiderrapante, cadeira de banho e campainha de chamada: os itens que eu mostro '
        'nos vídeos, com o que conferir antes de comprar. Links de afiliado, por um técnico de enfermagem.')
if LINK_PRESSAO:
    DESC = DESC.replace('campainha de chamada', 'aparelho de pressão')

CSS = """<style>
.art p.aviso-af{border:2px solid var(--green);border-radius:10px;padding:14px 16px;background:var(--sheet);font:500 15px/1.5 var(--mono)}
.comodo{display:grid;gap:14px;margin-top:10px}
.comodo>p.intro{color:var(--ink-2)}
.prod{border:1px solid var(--rule);border-radius:10px;padding:18px 20px;background:var(--sheet);display:grid;gap:10px}
.prod h3{font-size:24px;line-height:1.2;margin:0}
.prod .modelo{font:600 15px/1.4 var(--mono);color:var(--green);margin:0}
.prod p{margin:0;font-size:18px;line-height:1.6}
.prod details{border-top:1px solid var(--rule);padding-top:10px}
.prod summary{cursor:pointer;font-weight:700;font-size:16px}
.prod details p{margin-top:8px;color:var(--ink-2);font-size:17px}
.prod .btn{justify-self:start;min-height:48px;display:inline-flex;align-items:center}
</style>"""

jsonld = {"@context": "https://schema.org", "@graph": [
  {"@type": "WebPage", "name": TITULO, "description": DESC, "inLanguage": "pt-BR",
   "datePublished": HOJE, "dateModified": HOJE, "author": PERSON,
   "mainEntityOfPage": BASE + PATH, "image": BASE + "/foto.jpg",
   "citation": [u for _, u in FONTES]},
  {"@type": "ItemList", "name": "Itens para deixar a casa do idoso mais segura",
   "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": it["nome"]}
                       for i, it in enumerate(it for _, _, itens in COMODOS for it in itens)]},
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
    "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}

resumo = ''.join(f'<li>{r}</li>' for r in RESUMO)
faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
fontes = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in FONTES)
outros = ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in GUIAS_LINKS)

comodos = ''
COMODOS = [(n, i, [it for it in itens if it.get('link')]) for n, i, itens in COMODOS]
COMODOS = [c for c in COMODOS if c[2]]
for nome, intro, itens in COMODOS:
    cards = ''
    for it in itens:
        cards += f"""<article class="prod">
<h3>{it['nome']}</h3>
<p class="modelo">{it['modelo']}</p>
<p>{it['porque']}</p>
<details><summary>O que conferir antes de comprar</summary><p>{it['conferir']}</p></details>
<a class="btn on" href="{it['link']}" target="_blank" rel="noopener sponsored">Ver no Mercado Livre →</a>
</article>"""
    comodos += f"""<h2>{nome}</h2><div class="comodo"><p class="intro">{intro}</p>{cards}</div>"""

html = head(TITULO + ' | Anderson Costa', DESC, PATH, jsonld) + CSS + f"""
<header class="mini"><div class="wrap"><span>ANDERSON COSTA · {CRED.upper()}</span><a href="/">← Início</a></div></header>
<main class="wrap"><div class="crumb"><a href="/">Início</a> / Casa segura</div>
<article class="art">
<span class="tag" style="color:var(--green)">Casa segura</span>
<h1>Casa segura para o idoso</h1>
{AUTHOR_BOX}
<p class="aviso-af">Links de afiliado: eu recebo uma comissão se você comprar por eles, sem custo extra para você. Indico o que eu usaria, não o que paga mais.</p>
<div class="resumo"><span class="tag">Resumo rápido</span><ul>{resumo}</ul></div>
<p>Os itens abaixo são os que aparecem nos meus vídeos sobre prevenção de quedas e cuidado em casa. Em cada um está o que conferir antes de comprar, porque o detalhe errado anula o item: barra fixada com ventosa, tapete que vira tropeço, cadeira de banho com a roda destravada.' + ('' if not LINK_PRESSAO else '')+'</p>
<p>Antes de gastar, leia o <a href="/guias/como-evitar-queda-de-idoso-em-casa/">guia de prevenção de quedas</a>. A maior parte do que reduz risco em casa não custa nada.</p>
{comodos}
<h2>Perguntas frequentes</h2><div class="faq">{faq}</div>
<h2>Fontes</h2><ul>{fontes}</ul>
<p class="note">Conteúdo educativo. Não substitui a avaliação da equipe de saúde que acompanha a pessoa, e não indico medicamento nem suplemento. Em emergência, ligue 192.</p>
<h2>Leia também</h2><ul>{outros}</ul>
</article></main>""" + FOOT

os.makedirs(DIST + PATH, exist_ok=True)
open(DIST + PATH + 'index.html', 'w').write(html)

# 404, robots, sitemap, CNAME
open(os.path.join(DIST, '404.html'), 'w').write(head('Página não encontrada | Anderson Costa', 'Página não encontrada.', '/404.html', {"@context": "https://schema.org", "@type": "WebPage"}) +
    '<main class="wrap art"><h1>Página não encontrada</h1><p><a href="/">Voltar ao início</a></p></main></body></html>')
open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
urls = ['/'] + [f"/guias/{g['slug']}/" for g in GUIAS] + ['/casa-segura/']
open(os.path.join(DIST, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{BASE}{u}</loc><lastmod>{HOJE}</lastmod></url>\n' for u in urls) + '</urlset>\n')
if not DOMAIN.endswith('github.io'): open(os.path.join(DIST, 'CNAME'), 'w').write(DOMAIN + '\n')
print('ok', urls)

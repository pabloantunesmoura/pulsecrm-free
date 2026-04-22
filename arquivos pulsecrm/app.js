const navigationItems = [
  "Dashboard",
  "Leads",
  "Pipeline",
  "Agenda",
  "Mensagens",
  "Automacoes",
  "Campanhas",
  "Relatorios",
  "Equipes",
  "Integracoes",
  "Configuracoes"
];

const kpis = [
  { label: "MRR previsto", value: "R$ 482 mil", delta: "+12,4% vs mes anterior" },
  { label: "Leads qualificados", value: "1.248", delta: "+18% em 30 dias" },
  { label: "Tempo medio de resposta", value: "6m 12s", delta: "-22% com automacao" },
  { label: "Taxa de ganho", value: "29,7%", delta: "+4,1 p.p." }
];

const pipeline = [
  {
    stage: "Entrada",
    deals: [
      { name: "Grupo Orion", value: "R$ 120 mil", note: "Origem: Meta Ads" },
      { name: "Lume Retail", value: "R$ 64 mil", note: "Novo contato hoje" }
    ]
  },
  {
    stage: "Qualificacao",
    deals: [
      { name: "Nova Atria", value: "R$ 88 mil", note: "Lead score 91" },
      { name: "Vita Solar", value: "R$ 135 mil", note: "Sem resposta ha 2 dias" }
    ]
  },
  {
    stage: "Proposta",
    deals: [
      { name: "Atlas Foods", value: "R$ 210 mil", note: "Reuniao amanha 14:00" },
      { name: "Hexa Log", value: "R$ 96 mil", note: "Contrato em revisao" }
    ]
  },
  {
    stage: "Fechamento",
    deals: [
      { name: "Urban Pulse", value: "R$ 320 mil", note: "Probabilidade 80%" },
      { name: "Celta Med", value: "R$ 146 mil", note: "Aguardando assinatura" }
    ]
  }
];

const automations = [
  { name: "Boas-vindas WhatsApp", detail: "Disparo imediato apos captura do lead", tag: "Ativo" },
  { name: "Reengajamento sem resposta", detail: "3 toques em 5 dias com troca de canal", tag: "Performance" },
  { name: "Agendamento pos-proposta", detail: "Cria tarefa, e-mail e evento no Calendar", tag: "SLA" }
];

const schedule = [
  { name: "Daily comercial", detail: "09:00 • Time SDR", tag: "Equipe" },
  { name: "Demo Atlas Foods", detail: "14:00 • Mariana e Joao", tag: "Pipeline" },
  { name: "Follow-up Celta Med", detail: "16:30 • WhatsApp automatizado", tag: "Automacao" }
];

const channelPerformance = [
  { label: "WhatsApp", value: 86, amount: "86%" },
  { label: "Email", value: 68, amount: "68%" },
  { label: "Inbound", value: 74, amount: "74%" },
  { label: "Ads", value: 59, amount: "59%" }
];

const webFeatures = [
  {
    title: "Dashboard executivo em tempo real",
    text: "KPIs, forecast, perdas, ranking e produtividade com filtros por periodo, equipe, campanha e etapa."
  },
  {
    title: "Pipeline personalizavel",
    text: "Multiplos funis, SLA por etapa, motivos de perda e gatilhos automaticos por evento."
  },
  {
    title: "Operacao comercial unificada",
    text: "Leads, mensagens, agenda, tarefas e historico em uma unica linha do tempo."
  }
];

const mobileCards = [
  {
    title: "Tarefas do dia",
    text: "9 tarefas abertas, 3 com vencimento em ate 1h."
  },
  {
    title: "Pipeline prioritario",
    text: "4 oportunidades acima de R$ 100 mil aguardando proximo passo."
  },
  {
    title: "Inbox ativo",
    text: "11 mensagens novas em WhatsApp e 4 respostas por e-mail."
  }
];

function renderNavigation() {
  const nav = document.getElementById("nav-list");
  nav.innerHTML = navigationItems
    .map((item, index) => `<button class="nav-item ${index === 0 ? "is-active" : ""}">${item}</button>`)
    .join("");
}

function renderKpis() {
  const container = document.getElementById("kpi-grid");
  container.innerHTML = kpis
    .map(
      (item) => `
        <article class="panel kpi-card">
          <p class="eyebrow">${item.label}</p>
          <strong>${item.value}</strong>
          <span class="delta">${item.delta}</span>
        </article>
      `
    )
    .join("");
}

function renderPipeline() {
  const container = document.getElementById("pipeline-board");
  container.innerHTML = pipeline
    .map(
      (stage) => `
        <section class="stage-column">
          <h4>${stage.stage}</h4>
          ${stage.deals
            .map(
              (deal) => `
                <article class="deal-card">
                  <strong>${deal.name}</strong>
                  <span>${deal.value}</span>
                  <p>${deal.note}</p>
                </article>
              `
            )
            .join("")}
        </section>
      `
    )
    .join("");
}

function renderStackList(targetId, items) {
  const container = document.getElementById(targetId);
  container.innerHTML = items
    .map(
      (item) => `
        <article class="stack-item">
          <div>
            <strong>${item.name}</strong>
            <span>${item.detail}</span>
          </div>
          <span class="tag">${item.tag}</span>
        </article>
      `
    )
    .join("");
}

function renderChannelPerformance() {
  const container = document.getElementById("channel-chart");
  container.innerHTML = channelPerformance
    .map(
      (row) => `
        <div class="bar-row">
          <strong>${row.label}</strong>
          <div class="bar-track">
            <div class="bar-fill" style="width:${row.value}%"></div>
          </div>
          <span>${row.amount}</span>
        </div>
      `
    )
    .join("");
}

function renderFeatures() {
  const container = document.getElementById("web-features");
  container.innerHTML = webFeatures
    .map(
      (item) => `
        <article class="feature-item">
          <div>
            <strong>${item.title}</strong>
            <span>${item.text}</span>
          </div>
        </article>
      `
    )
    .join("");
}

function renderMobileCards() {
  const container = document.getElementById("mobile-cards");
  container.innerHTML = mobileCards
    .map(
      (item) => `
        <article class="mobile-card">
          <div>
            <strong>${item.title}</strong>
            <span>${item.text}</span>
          </div>
        </article>
      `
    )
    .join("");
}

renderNavigation();
renderKpis();
renderPipeline();
renderStackList("automation-list", automations);
renderStackList("schedule-list", schedule);
renderChannelPerformance();
renderFeatures();
renderMobileCards();

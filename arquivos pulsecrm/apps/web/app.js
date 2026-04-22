const state = {
  auth: null,
  bootstrap: null,
  publicUsers: [],
  publicInvitation: null
};

const navigationItems = [
  { key: "dashboard", label: "Dashboard" },
  { key: "leads", label: "Leads" },
  { key: "pipeline", label: "Pipeline" },
  { key: "agenda", label: "Agenda" },
  { key: "automacoes", label: "Automacoes" },
  { key: "configuracoes", label: "Configuracoes" }
];

function setAuthenticatedUi(isAuthenticated) {
  const newLeadButton = document.getElementById("new-lead-button");
  const inviteForm = document.getElementById("invite-form");
  newLeadButton.disabled = !isAuthenticated;
  Array.from(inviteForm.elements).forEach((element) => {
    element.disabled = !isAuthenticated;
  });
}

async function api(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(state.auth?.token ? { Authorization: `Bearer ${state.auth.token}` } : {})
  };
  const response = await fetch(path, {
    headers,
    ...options
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: "Erro desconhecido" }));
    throw new Error(error.message || "Falha na requisicao");
  }

  return response.json();
}

function renderNavigation() {
  const nav = document.getElementById("nav-list");
  nav.innerHTML = navigationItems
    .map(
      (item, index) =>
        `<button class="nav-item ${index === 0 ? "is-active" : ""}" data-key="${item.key}">${item.label}</button>`
    )
    .join("");
}

function renderLoginOptions(users) {
  const select = document.getElementById("login-email");
  select.innerHTML = users
    .map((user) => `<option value="${user.email}">${user.name} • ${user.role}</option>`)
    .join("");
}

function renderMetrics(metrics) {
  const container = document.getElementById("metrics");
  container.innerHTML = metrics
    .map(
      (metric) => `
        <article class="metric-card">
          <p class="eyebrow">${metric.label}</p>
          <strong>${metric.value}</strong>
          <span class="badge">${metric.trend}</span>
        </article>
      `
    )
    .join("");
}

function renderLeads(leads) {
  const rows = document.getElementById("lead-rows");
  rows.innerHTML = leads
    .map(
      (lead) => `
        <tr>
          <td>
            <div class="lead-name">
              <strong>${lead.name}</strong>
              <span>${lead.owner}</span>
            </div>
          </td>
          <td>${lead.company}</td>
          <td>${lead.source}</td>
          <td>${lead.score}</td>
          <td>${lead.stage}</td>
          <td>
            <div class="lead-name">
              <span>${lead.nextAction}</span>
              <div class="chip-list">${lead.tags.map((tag) => `<span class="chip">${tag}</span>`).join("")}</div>
            </div>
          </td>
        </tr>
      `
    )
    .join("");
}

function renderAgenda(items) {
  const container = document.getElementById("agenda-list");
  container.innerHTML = items
    .map(
      (item) => `
        <article class="stack-item">
          <div>
            <strong>${item.title}</strong>
            <span>${new Date(item.startsAt).toLocaleString("pt-BR")} • ${item.owner}</span>
          </div>
          <span class="badge">${item.type}</span>
        </article>
      `
    )
    .join("");
}

function renderPipeline(stages) {
  const board = document.getElementById("pipeline-board");
  board.innerHTML = stages
    .map(
      (stage) => `
        <section class="stage">
          <h4>${stage.name}</h4>
          ${stage.deals
            .map(
              (deal) => `
                <article class="deal-card">
                  <strong>${deal.title}</strong>
                  <span>R$ ${Number(deal.value).toLocaleString("pt-BR")}</span>
                  <p>${deal.owner} • Fecha em ${new Date(deal.expectedCloseAt).toLocaleDateString("pt-BR")}</p>
                </article>
              `
            )
            .join("")}
        </section>
      `
    )
    .join("");
}

function renderAutomations(items) {
  const container = document.getElementById("automation-list");
  container.innerHTML = items
    .map(
      (item) => `
        <article class="stack-item">
          <div>
            <strong>${item.name}</strong>
            <span>${item.description}</span>
          </div>
          <span class="badge">${item.channel}</span>
        </article>
      `
    )
    .join("");
}

function renderActivity(items) {
  const container = document.getElementById("activity-list");
  container.innerHTML = items
    .map(
      (item) => `
        <article class="timeline-item">
          <span class="timeline-dot"></span>
          <div>
            <strong>${item.type}</strong>
            <span>${item.summary}</span>
          </div>
          <span>${new Date(item.at).toLocaleString("pt-BR")}</span>
        </article>
      `
    )
    .join("");
}

function renderTeam(users) {
  const container = document.getElementById("team-list");
  container.innerHTML = users
    .map(
      (user) => `
        <article class="stack-item">
          <div>
            <strong>${user.name}</strong>
            <span>${user.title}</span>
          </div>
          <span class="badge">${user.role}</span>
        </article>
      `
    )
    .join("");
}

function renderInviteRoles(roles) {
  const select = document.getElementById("invite-role");
  select.innerHTML = roles
    .map((role) => `<option value="${role.id}">${role.name}</option>`)
    .join("");
}

function renderInvites(items) {
  const container = document.getElementById("invite-list");
  container.innerHTML = items
    .map(
      (item) => `
        <article class="stack-item">
          <div>
            <strong>${item.email}</strong>
            <span>${item.role_name} • convidado por ${item.inviter_name}</span>
            <span>${window.location.origin}/?invite=${item.invite_token}</span>
          </div>
          <span class="badge">${item.status}</span>
        </article>
      `
    )
    .join("");
}

function renderMobile(leads, tasks) {
  const container = document.getElementById("mobile-preview");
  const topLead = leads[0];
  const pendingTasks = tasks.filter((task) => task.status !== "DONE").slice(0, 2);

  container.innerHTML = `
    <div class="phone-card">
      <span class="eyebrow">Hoje</span>
      <strong>Operacao do vendedor</strong>
      <p>${state.auth?.user?.name || "Usuario"} • ${state.auth?.user?.role || "Equipe"}</p>
    </div>
    <div class="phone-card">
      <span class="eyebrow">Prioridade</span>
      <strong>${topLead?.company || "Sem leads"}</strong>
      <p>${topLead?.nextAction || "Base em sincronizacao."}</p>
    </div>
    ${pendingTasks
      .map(
        (task) => `
          <div class="phone-card">
            <span class="eyebrow">${task.priority}</span>
            <strong>${task.title}</strong>
            <p>Prazo ${new Date(task.dueAt).toLocaleString("pt-BR")}</p>
          </div>
        `
      )
      .join("")}
  `;
}

function renderBootstrap(data) {
  state.bootstrap = data;
  document.getElementById("tenant-name").textContent = `${data.tenant.name} • Plano ${data.tenant.plan}`;
  renderMetrics(data.dashboard.metrics);
  renderLeads(data.leads);
  renderAgenda(data.agenda);
  renderPipeline(data.pipeline);
  renderAutomations(data.automations);
  renderActivity(data.activity);
  renderTeam(data.users);
  renderInviteRoles(data.roles);
  renderInvites(data.invitations);
  renderMobile(data.leads, data.tasks);
}

function renderPublicInvitation(invite) {
  const card = document.getElementById("invite-accept-card");
  const tenant = document.getElementById("invite-tenant");
  const summary = document.getElementById("invite-summary");
  const email = document.getElementById("accept-email");
  const feedback = document.getElementById("invite-feedback");
  const form = document.getElementById("accept-invite-form");

  if (!invite) {
    card.hidden = true;
    return;
  }

  card.hidden = false;
  tenant.textContent = invite.tenantName;
  summary.textContent = `${invite.inviterName} convidou você como ${invite.roleName}.`;
  email.value = invite.email;
  Array.from(form.elements).forEach((element) => {
    if (element.id === "accept-email") {
      element.disabled = true;
      return;
    }
    element.disabled = invite.status !== "PENDING";
  });
  feedback.textContent =
    invite.status === "PENDING"
      ? "Preencha seus dados para entrar no workspace gratuito."
      : "Este convite já foi utilizado.";
}

async function loadBootstrap() {
  const data = await api("/api/bootstrap");
  renderBootstrap(data);
}

async function loadPublicUsers() {
  const data = await api("/api/public/users");
  state.publicUsers = data.items;
  renderLoginOptions(data.items);
}

async function loadPublicInvitation() {
  const inviteToken = new URLSearchParams(window.location.search).get("invite");
  if (!inviteToken) {
    renderPublicInvitation(null);
    return;
  }

  try {
    const data = await api(`/api/public/invitations/${inviteToken}`);
    state.publicInvitation = data.item;
    renderPublicInvitation(data.item);
  } catch (error) {
    state.publicInvitation = {
      inviteToken,
      tenantName: "Convite invalido",
      inviterName: "PulseCRM",
      roleName: "Convidado",
      email: "",
      status: "INVALID"
    };
    renderPublicInvitation(state.publicInvitation);
    document.getElementById("invite-summary").textContent = error.message;
    document.getElementById("invite-feedback").textContent =
      "Peça um novo link para quem compartilhou o workspace com você.";
  }
}

async function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;
  const payload = await api("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });

  state.auth = payload;
  document.getElementById("page-title").textContent = `Dashboard executivo • ${payload.user.role}`;
  setAuthenticatedUi(true);
  await loadBootstrap();
}

async function acceptInvitation(payload) {
  const session = await api("/api/public/accept-invitation", {
    method: "POST",
    body: JSON.stringify(payload)
  });

  state.auth = session;
  document.getElementById("page-title").textContent = `Dashboard executivo • ${session.user.role}`;
  setAuthenticatedUi(true);
  await loadPublicUsers();
  await loadPublicInvitation();
  await loadBootstrap();
}

function bindDialog() {
  const dialog = document.getElementById("lead-dialog");
  const button = document.getElementById("new-lead-button");
  const form = document.getElementById("lead-form");

  button.addEventListener("click", () => dialog.showModal());

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    await api("/api/leads", {
      method: "POST",
      body: JSON.stringify(payload)
    });

    dialog.close();
    form.reset();
    await loadBootstrap();
  });
}

function bindActions() {
  document.getElementById("login-button").addEventListener("click", login);
  document.getElementById("seed-button").addEventListener("click", async () => {
    if (!state.auth) {
      await loadPublicUsers();
      return;
    }
    await loadBootstrap();
  });
}

function bindInviteForm() {
  const form = document.getElementById("invite-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!state.auth) {
      return;
    }

    const payload = Object.fromEntries(new FormData(form).entries());
    await api("/api/invitations", {
      method: "POST",
      body: JSON.stringify(payload)
    });
    form.reset();
    await loadBootstrap();
  });
}

function bindAcceptInviteForm() {
  const form = document.getElementById("accept-invite-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!state.publicInvitation || state.publicInvitation.status !== "PENDING") {
      return;
    }

    const payload = Object.fromEntries(new FormData(form).entries());
    payload.inviteToken = state.publicInvitation.inviteToken;
    payload.email = state.publicInvitation.email;
    await acceptInvitation(payload);
  });
}

renderNavigation();
setAuthenticatedUi(false);
bindDialog();
bindActions();
bindInviteForm();
bindAcceptInviteForm();
Promise.all([loadPublicUsers(), loadPublicInvitation()]).catch((error) => {
  document.getElementById("tenant-name").textContent = error.message;
});

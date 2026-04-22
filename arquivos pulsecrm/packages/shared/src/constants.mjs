export const navigation = [
  "dashboard",
  "leads",
  "pipeline",
  "agenda",
  "automacoes",
  "configuracoes"
];

export const roleCapabilities = {
  Administrador: ["all"],
  Gestor: ["team:read", "team:assign", "reports:read"],
  Vendedor: ["portfolio:read", "portfolio:update", "tasks:manage"],
  Suporte: ["assigned:read", "inbox:manage"]
};

export const defaultLeadPayload = {
  company: "",
  name: "",
  email: "",
  phone: "",
  source: "Manual",
  status: "NEW",
  score: 50,
  stageId: "stage-entry",
  tags: [],
  nextAction: "",
  notes: ""
};

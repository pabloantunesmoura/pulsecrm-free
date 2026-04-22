# Publicacao Rapida

Use este roteiro para colocar o PulseCRM online no Render.

## 1. Publicar o codigo no GitHub

No seu computador com Git configurado:

```powershell
git init
git add .
git commit -m "Prepare PulseCRM for free web deploy"
git branch -M main
git remote add origin <SEU_REPOSITORIO_GITHUB>
git push -u origin main
```

## 2. Criar o deploy no Render

1. Entre em [dashboard.render.com](https://dashboard.render.com)
2. Clique em `New`
3. Escolha `Blueprint`
4. Conecte o repositorio do GitHub
5. Selecione a branch `main`
6. Confirme o blueprint encontrado em `render.yaml`
7. Clique para criar os recursos

## 3. Aguardar a provisao

O Render deve criar:

- `pulsecrm-free` como web service Python
- `pulsecrm-db` como banco PostgreSQL

## 4. Testar online

1. Abra a URL publica do serviço
2. Faça login com `ana@pulsecrm.demo` / `demo123`
3. Gere um convite
4. Abra o link `/?invite=<token>`
5. Crie a conta do convidado

## 5. Validacao minima

- `GET /api/health` responde `ok`
- dashboard carrega
- novo lead salva
- convite cria
- convite aceita

## Observacao

Se o Render exibir limite ou indisponibilidade do banco gratuito, mantenha o deploy do app e substitua o banco por um Postgres externo.

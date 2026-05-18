# Hominun RPG — Mods

Esta pasta reserva o espaço para o sistema de mods futuro.

## Contrato público (rascunho)

Um mod é uma pasta com a seguinte estrutura mínima:

```
mods/
└── meu_mod/
    ├── mod.json          # Metadados: id, nome, versão, autor, dependências
    ├── data/             # Conteúdo adicional: diálogos, criaturas, regiões, itens
    ├── assets/           # Assets do mod: portraits, áudio, efeitos
    └── scripts/          # (futuro) Lógica de mod via sandbox seguro
```

## mod.json mínimo

```json
{
  "id": "meu_mod",
  "name": "Meu Mod",
  "version": "1.0.0",
  "author": "",
  "game_version_min": "1.0.0",
  "dependencies": []
}
```

## Regras

- Mods NÃO podem sobrescrever lógica de domínio do servidor.
- Mods podem adicionar conteúdo data-driven (JSON/YAML).
- O content pipeline valida mods com os mesmos schemas do jogo base.

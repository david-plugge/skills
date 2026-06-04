# CONTEXT.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

## Single vs multi-context repos

**Single context (most repos):** One `CONTEXT.md` at the repo root.

**Multiple contexts:** A `CONTEXT-MAP.md` at the repo root lists the contexts, where they live, and how they relate to each other:

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

The skill infers which structure applies:

- If `CONTEXT-MAP.md` exists, read it to find contexts.
- If only a root `CONTEXT.md` exists, single context.
- If neither exists, make the lazy placement decision below the first time a term is resolved.

When multiple contexts exist, infer which one the current topic relates to. If unclear, ask.

### Choosing the layout (when neither file exists)

The placement decision is lazy — make it the moment you're about to write the first term, from the repo's actual shape.

1. **Default to a single root `CONTEXT.md`.** Most repos want this — including monorepos whose packages are just layers of one product (a `web` + `api` for the same app share one domain).
2. **Choose multi-context only when two things are both true:** the repo holds genuinely separate domains (not just layers), _and_ the term you're resolving clearly belongs to one of them. Signals of separate domains: a workspace manifest (`pnpm-workspace.yaml`, `workspaces` in `package.json`, a Cargo/Go workspace) whose packages own distinct domain logic — `ordering` and `billing`, not `frontend` and `backend`.
3. **When you go multi-context, create the map in the same step.** Write the term into that context's `CONTEXT.md` (e.g. `packages/ordering/CONTEXT.md`) and create the root `CONTEXT-MAP.md` — the map is what tells every future run the repo is multi-context and where each context lives. A single-entry map is fine; it grows as contexts appear.

**Promoting single → multi.** If a root `CONTEXT.md` already exists and you hit a term that clearly belongs to a distinct _second_ domain, don't cram it in. Split: move that glossary's context-specific terms into per-context `CONTEXT.md` files, keep genuinely shared terms reachable via the map, and introduce the `CONTEXT-MAP.md`. Only do this when a real second context appears — one context never needs a map.

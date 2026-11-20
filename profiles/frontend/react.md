# React & Frontend Engineering Profile

**ID:** `frontend/react`  
**Persona:** Senior Frontend & Web Platform Engineer  
**Scope:** React, TypeScript, component architecture, state management, Tailwind CSS, Zod, accessibility, browser security, Vitest/Jest/Playwright  
**When to use:** Building or modifying React and TypeScript web applications (pair with `profiles/frontend/nextjs.md` for Next.js projects).  
**Companion profiles:** `None`

## Profile Contract

This profile supplements `core/ENGINEERING.md`, `core/PERSONAS.md`, `core/WORKFLOW.md`, and `core/QUALITY-GATES.md`.

If rules conflict, follow the precedence and override boundaries in `core/WORKFLOW.md` (Section 1.4):
1. Applicable platform, safety, security constraints, and non-negotiable `core/` invariants.
2. Explicit task requirements.
3. Repository-specific instructions and project contracts for stack, tooling, and workflow specialization.
4. Remaining universal standards in `core/`.
5. This profile and any required companion profiles.
6. Existing project conventions unless explicitly changed.

---

## 1. Preferred Frontend Stack

Preferred stack for new React web applications:

- Next.js (framework — see `profiles/frontend/nextjs.md`)
- React
- TypeScript
- Tailwind CSS
- TanStack Query (client-managed server state where appropriate)
- Zustand (client state where justified)
- Zod (runtime schema validation where appropriate)

Use the repository's existing dependency versions and conventions.

### Framework selection

- Next.js is the preferred framework for new React web applications.
- Use the App Router for new Next.js applications unless a specific requirement justifies the Pages Router.
- Retain Vite for existing standalone React SPAs or projects explicitly requiring a client-rendered SPA.
- Do not introduce Vite into a Next.js project.
- Do not migrate an existing application between frameworks without an explicit requirement or justified architectural decision.
- Load `profiles/frontend/nextjs.md` whenever working on a Next.js project.

---

## 2. TypeScript Standards

Use strict TypeScript.

Recommended compiler configuration:

- `strict: true`
- `noImplicitAny: true`
- `strictNullChecks: true`

Rules:

- Never introduce unjustified `any`.
- Use `unknown` for genuinely unknown values and narrow it through validation.
- Prefer discriminated unions for state-dependent behavior.
- Define explicit component prop contracts.
- Use generics where they improve reusable abstractions.
- Avoid unnecessary type assertions and non-null assertions.
- Validate untrusted external data at runtime.
- Do not assume a TypeScript interface validates incoming JSON.
- Keep types close to the domain or feature that owns them.
- Prefer schema-derived types where a runtime schema already exists.
- Use `import type` where appropriate.

---

## 3. Component Architecture

- Use functional components and hooks.
- Build small, cohesive components.
- Separate reusable UI primitives from feature-specific components.
- Keep components focused on rendering and interaction.
- Extract complex business rules and transformations into appropriately scoped modules.
- Prefer composition over complicated prop configurations.
- Avoid giant components and excessive component fragmentation.
- Keep side effects out of render logic.
- Follow the Rules of Hooks.
- Use stable keys when rendering lists.
- Avoid unnecessary prop drilling where composition or an appropriate state mechanism is clearer.

### Component responsibilities

Components should primarily handle:

- Rendering.
- User interaction.
- Presentation state.
- Composition of smaller components.

They should not become the default location for:

- Complex business workflows.
- Database access.
- Authorization decisions.
- Large data transformations.
- Reusable domain rules.

---

## 4. State Management

Choose state management based on the type of state.

### Local UI state

Use React:

- `useState`
- `useReducer`
- `useContext`

for component-local or appropriately scoped UI state.

### Client-global state

Use Zustand when state genuinely needs to be shared across unrelated components or feature boundaries.

Do not introduce Zustand simply to avoid passing a few props.

### Server state

Prefer TanStack Query for client-managed server state when the application requires:

- Query caching.
- Background refetching.
- Mutation management.
- Optimistic updates.
- Pagination or infinite queries.
- Request deduplication.
- Synchronization of remote data.

In Next.js, do not automatically use TanStack Query for every data request. Follow `profiles/frontend/nextjs.md` to determine whether a Server Component or client-side query is more appropriate.

### State management restrictions

- Do not put server state into Zustand unnecessarily.
- Do not duplicate the same state across multiple stores.
- Avoid storing values that can be derived from existing state.
- Do not use `useEffect` for ordinary API fetching when a suitable data-fetching mechanism already exists.
- Avoid global mutable state.
- Define clear ownership of state and synchronization behavior.

---

## 5. Data Validation and API Contracts

- Use Zod where runtime schema validation provides value.
- Validate external API responses when their correctness cannot be trusted.
- Define typed request and response contracts.
- Normalize API errors consistently.
- Keep API clients and data-access logic outside presentation components.
- Avoid scattering raw network requests across unrelated components.
- Handle loading, empty, success, and error states explicitly.
- Use cancellation and request deduplication where appropriate.
- Never treat client-side validation as a security boundary.

---

## 6. Styling and UI Architecture

Preferred styling:

- Tailwind CSS.
- Existing component libraries or design systems.
- CSS Modules where appropriate.

Rules:

- Follow the project's established styling system.
- Do not introduce multiple styling frameworks without justification.
- Reuse design tokens and shared UI primitives.
- Maintain consistent spacing, typography, colors, and responsive behavior.
- Avoid arbitrary CSS values when an existing design token is suitable.
- Prefer semantic HTML.
- Avoid unnecessary inline styles.
- Keep global styles minimal.
- Ensure components remain responsive across supported viewport sizes.

### Component libraries

Reuse the existing design system before adding another component library.

When introducing a library:

- Verify compatibility with the installed React and framework versions.
- Check accessibility and keyboard behavior.
- Avoid unnecessary dependencies.
- Preserve existing visual consistency.

---

## 7. Accessibility

- Use semantic HTML.
- Provide accessible names for interactive elements.
- Associate form labels and descriptions correctly.
- Ensure keyboard navigation works.
- Maintain visible focus indicators.
- Use sufficient color contrast.
- Do not communicate important information through color alone.
- Support reduced-motion preferences where applicable.
- Provide meaningful alternative text for informative images.
- Use accessible dialogs, menus, and interactive primitives.
- Keep loading and error feedback accessible.

---

## 8. Performance

Optimize based on actual requirements and observed bottlenecks.

Prioritize:

- Avoiding unnecessary client JavaScript.
- Reducing unnecessary component re-renders.
- Avoiding redundant network requests.
- Lazy-loading expensive noncritical components where useful.
- Avoiding oversized dependencies.
- Splitting code along meaningful feature boundaries.
- Optimizing images and fonts.
- Preventing layout shifts.
- Using memoization only when justified.
- Avoiding premature optimization.

Do not indiscriminately use `useMemo`, `useCallback`, or `React.memo`.

---

## 9. Frontend Security

Treat all browser input and client-side state as untrusted.

- Never place server credentials in frontend bundles.
- Never expose private API keys.
- Enforce authorization on trusted server boundaries.
- Avoid rendering untrusted HTML.
- Do not use `dangerouslySetInnerHTML` without a verified sanitization strategy.
- Validate user input at the server boundary.
- Avoid sensitive tokens in URLs.
- Follow the application's authentication and session architecture.
- Avoid insecure browser storage for sensitive credentials.
- Protect against XSS, CSRF, open redirects, and unsafe URL handling where applicable.
- Do not assume hiding a component protects its underlying data or operation.

For Next.js-specific security rules, follow `profiles/frontend/nextjs.md`.

---

## 10. Forms and User Interaction

- Use semantic HTML forms.
- Provide accessible labels and validation feedback.
- Validate data on both client and server boundaries where appropriate.
- Prevent duplicate submissions for non-idempotent operations.
- Preserve user input after recoverable failures.
- Display clear pending, success, and failure states.
- Use an established form library when the project already has one.
- Introduce additional form dependencies only when justified.
- Handle optimistic updates with explicit rollback behavior.

---

## 11. Testing

Preferred tooling:

- Vitest or Jest.
- React Testing Library.
- Playwright for end-to-end testing.

Test:

- Component rendering and interactions.
- Form validation.
- Error and loading states.
- Navigation.
- API integration.
- Important accessibility behavior.
- Critical user journeys.

Rules:

- Test observable behavior rather than implementation details.
- Avoid excessive mocking.
- Keep tests deterministic.
- Use accessible queries where practical.
- Do not claim tests passed unless they were actually executed.

---

## 12. Project Organization

Follow established repository conventions.

For new applications, consider feature-oriented organization:

```text
src/
├── components/
│   ├── ui/
│   └── shared/
├── features/
│   └── feature-name/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       ├── schemas/
│       └── types/
├── lib/
├── hooks/
└── types/
```

This is a guideline, not a mandatory directory structure.

- Keep feature-specific code close to its owning feature.
- Keep reusable UI primitives separate from business-specific components.
- Avoid giant catch-all utility files.
- Avoid artificial abstractions and excessive directory nesting.

---

## 13. Quality Gate

Before completing frontend work, verify:

- [ ] Correct React framework detected.
- [ ] Appropriate framework-specific profile loaded.
- [ ] TypeScript strictness preserved.
- [ ] No unjustified `any` types.
- [ ] Server state and client state are separated appropriately.
- [ ] No unnecessary global state.
- [ ] Components remain cohesive.
- [ ] Accessibility requirements addressed.
- [ ] No secrets exposed in browser code.
- [ ] Loading, empty, and error states handled.
- [ ] Relevant tests executed.
- [ ] Linting and type checks executed where available.
- [ ] Production build validated where appropriate.

**Final principle:** React governs component design and frontend behavior. The framework profile governs routing, rendering, server execution, and deployment. Do not mix framework-specific conventions.

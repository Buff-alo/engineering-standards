# Next.js Engineering Profile

**ID:** `frontend/nextjs`  
**Persona:** Senior Next.js & Full-Stack Web Architect  
**Scope:** Next.js applications, App Router, Pages Router, React Server Components, Server Actions, Route Handlers, rendering, caching, data access, deployment  
**When to use:** Building or modifying Next.js applications (always compose with `profiles/frontend/react.md`).  
**Companion profiles:** `frontend/react.md`

## Profile Contract

This profile supplements `core/ENGINEERING.md`, `core/PERSONAS.md`, `core/WORKFLOW.md`, and `core/QUALITY-GATES.md`. It extends `profiles/frontend/react.md` and does not replace React component, TypeScript, accessibility, or frontend security standards.

If rules conflict, follow the precedence order in `core/WORKFLOW.md`:
1. Applicable platform, safety, and security constraints.
2. Explicit task requirements.
3. Repository-specific instructions and established project contracts.
4. Universal standards in `core/`.
5. This profile and `profiles/frontend/react.md`.
6. Existing project conventions unless explicitly changed.

---

## 1. Preferred Stack

Preferred stack for new Next.js applications:

- Next.js
- React
- TypeScript
- App Router
- Tailwind CSS
- TanStack Query where client-managed server state is justified
- Zustand where client-global state is justified
- Zod for runtime validation where appropriate

Use the versions already established by the project.

Do not assume the latest Next.js APIs are compatible with an existing application. Inspect `package.json`, lockfiles, and framework configuration first.

### Project requirements

- Prefer App Router for new projects.
- Preserve Pages Router in existing applications unless migration is explicitly requested.
- Do not mix App Router and Pages Router conventions unintentionally.
- Do not introduce a separate backend architecture without evaluating existing services and ownership boundaries.
- Use Next.js capabilities where they simplify the architecture, not merely because they exist.

---

## 2. Next.js Application Architecture

### App Router

Use the App Router for new applications.

Understand the responsibilities of:

- `app/` — route definitions and layouts.
- `page.tsx` — route-specific UI.
- `layout.tsx` — shared layout and nested composition.
- `loading.tsx` — loading boundaries.
- `error.tsx` — route-level error boundaries.
- `not-found.tsx` — not-found handling.
- `route.ts` — HTTP Route Handlers.
- Route groups — logical organization without changing URL structure.
- Dynamic segments — parameterized routes.
- Parallel and intercepted routes — only where their functionality is required.

Example:

```text
src/
├── app/
│   ├── (public)/
│   │   ├── page.tsx
│   │   └── about/
│   │       └── page.tsx
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   └── dashboard/
│   │       └── page.tsx
│   ├── api/
│   │   └── health/
│   │       └── route.ts
│   ├── layout.tsx
│   └── globals.css
├── components/
├── features/
├── lib/
└── types/
```

This is an example structure. Respect the existing repository.

### Pages Router

For existing Pages Router applications:

- Preserve `pages/` conventions.
- Use the appropriate data-fetching mechanisms for the installed version.
- Understand `getStaticProps`, `getServerSideProps`, and client-side fetching where applicable.
- Do not introduce App Router-only APIs into Pages Router files.
- Treat migration as a separate architectural task.

---

## 3. React Server Components and Client Components

This is a core architectural distinction in Next.js App Router.

### Server Components

Server Components are the default in the App Router.

Use them for:

- Initial page rendering.
- Server-side data retrieval.
- Accessing trusted internal services.
- Reading server-only configuration.
- Rendering content that does not require browser interaction.
- Reducing unnecessary client-side JavaScript.

Rules:

- Prefer Server Components unless browser interactivity is required.
- Keep database and privileged service access on the server.
- Do not import server-only modules into client-side module graphs.
- Avoid sending sensitive or unnecessarily large objects to Client Components.
- Pass only the data required by the client.
- Use `server-only` for modules that must remain server-side where appropriate.

### Client Components

Use `"use client"` only when the component requires:

- React state.
- Event handlers.
- Effects.
- Browser APIs.
- Client-side hooks.
- Client-side interactive libraries.

Rules:

- Keep client boundaries as narrow as practical.
- Do not mark an entire application or layout as a Client Component merely for convenience.
- Avoid importing large dependencies into client-side module graphs unnecessarily.
- Do not access `window`, `document`, or `localStorage` during server execution.
- Prevent hydration mismatches.
- Do not treat Client Components as trusted authorization boundaries.

### Component composition

- Server Components can render Client Components.
- Use composition to keep interactive components small.
- Pass serializable data across server/client boundaries.
- Do not pass server-only functions, database connections, or privileged objects to Client Components.
- Use the supported composition patterns for server-rendered content inside client-side interfaces.

---

## 4. Data Access Architecture

### Server-side data access

Prefer direct server-side data access from Server Components when appropriate.

Example:

```text
Server Component
      |
      v
Data Access Layer
      |
      v
Service / Repository
      |
      v
Database or External Service
```

Do not call your own Route Handler from a Server Component merely to access data that can be retrieved directly from the server-side data-access layer. This creates an unnecessary HTTP boundary and extra network overhead.

### Data Access Layer

For applications with meaningful business logic, centralize server-side data access.

Example:

```text
src/
├── lib/
│   ├── server/
│   │   ├── auth.ts
│   │   └── db.ts
│   └── validation/
├── features/
│   └── users/
│       ├── services/
│       ├── queries/
│       ├── schemas/
│       └── types/
└── app/
```

Rules:

- Keep database access out of presentation components.
- Separate data retrieval from business workflows when complexity justifies it.
- Avoid duplicating domain rules across Server Actions, Route Handlers, and UI components.
- Use explicit input and output contracts.
- Validate untrusted input at boundaries.
- Keep privileged data-access code server-only.

### Existing backend integration

If the project already uses Django, FastAPI, Spring Boot, Laravel, or another backend:

- Preserve backend ownership of domain logic and persistence unless explicitly changing the architecture.
- Do not duplicate business rules in Next.js.
- Keep backend credentials on the server.
- Choose direct server-to-server requests, Route Handlers, or client-side requests based on the security and execution requirements.
- Define clear API contracts.
- Handle backend timeouts, failures, and authentication explicitly.
- Avoid unnecessary HTTP hops.

---

## 5. Rendering Strategies

Choose rendering based on application requirements.

Understand:

- Static rendering.
- Dynamic rendering.
- Server-side rendering.
- Streaming.
- Client-side rendering.
- Incremental regeneration and revalidation where supported.

Evaluate:

- SEO requirements.
- Authentication and personalization.
- Data freshness.
- User experience.
- Performance.
- Hosting environment.
- Server resource consumption.
- Cacheability.

Do not force every route into one rendering strategy.

Use streaming and Suspense boundaries where they improve perceived performance and preserve a coherent loading experience.

---

## 6. Caching and Revalidation

Caching must be intentional.

Understand the installed Next.js version's caching semantics before implementing or modifying caching behavior.

Distinguish:

- Request memoization.
- Data caching.
- Rendered route or output caching.
- Client-side caching.
- CDN and infrastructure caching.

Rules:

- Never assume a request is cached without checking the version and configuration.
- Define freshness and invalidation requirements.
- Use supported revalidation mechanisms such as `revalidatePath` and `revalidateTag` where appropriate.
- Invalidate affected cached data after mutations.
- Avoid caching personalized responses in shared caches.
- Ensure tenant-specific and user-specific data cannot leak across requests.
- Understand how cookies, headers, authentication, and dynamic APIs affect caching.
- Document important caching decisions.

Do not add caching simply to improve perceived performance without understanding consistency implications.

---

## 7. Server Actions

Server Actions are server-side entry points that can be invoked by clients. Treat them as exposed application boundaries.

Rules:

- Authenticate the caller where required.
- Authorize every sensitive operation on the server.
- Validate every input.
- Enforce object-level and tenant-level access control.
- Never trust hidden buttons or client-side role checks.
- Keep domain logic in reusable service modules.
- Use transactions for workflows that require atomicity.
- Use idempotency for operations that may be retried.
- Return safe, typed responses.
- Avoid exposing internal exceptions or sensitive records.
- Revalidate affected data when appropriate.

Use Server Actions for suitable application mutations, not as a universal replacement for HTTP APIs.

---

## 8. Route Handlers

Use Route Handlers when a real HTTP boundary is needed.

Appropriate cases include:

- External API integrations.
- Webhooks.
- Mobile or third-party clients.
- Public HTTP endpoints.
- Browser-facing endpoints requiring an explicit API contract.

Rules:

- Define supported HTTP methods.
- Validate request bodies, parameters, and headers.
- Authenticate and authorize requests where required.
- Return appropriate HTTP status codes.
- Use stable response contracts.
- Apply rate limiting where appropriate.
- Set appropriate cache-control headers.
- Validate webhook signatures and protect against replay attacks.
- Enforce request-size limits where appropriate.
- Never expose stack traces or internal infrastructure details.
- Avoid duplicating business logic between Route Handlers and Server Actions.

---

## 9. Authentication and Authorization

Use established authentication solutions and the application's existing identity architecture.

Rules:

- Keep session validation on trusted server boundaries.
- Enforce authorization for every sensitive operation.
- Use secure, HttpOnly, appropriately configured cookies where cookie-based sessions are used.
- Apply SameSite and CSRF protections according to the authentication architecture.
- Never place credentials in URLs.
- Never expose private secrets through client bundles.
- Do not assume middleware or proxy-level route filtering replaces resource-level authorization.
- Protect against IDOR and tenant-isolation failures.
- Verify permissions again at the operation boundary.

For Next.js-specific request interception, use the terminology and APIs supported by the installed version. Do not blindly copy middleware or proxy examples across major versions.

---

## 10. Environment and Configuration

- Keep server-only secrets in server-side environment variables.
- Treat `NEXT_PUBLIC_` variables as public.
- Never put private credentials in `NEXT_PUBLIC_` variables.
- Validate required environment variables at appropriate startup or execution boundaries.
- Provide a safe `.env.example`.
- Do not commit `.env` files containing real secrets.
- Separate development, staging, and production configuration.
- Avoid accessing browser-only configuration from server modules.
- Do not expose database connection strings or internal service credentials.

---

## 11. Forms and Mutations

- Use semantic HTML forms.
- Use Server Actions or API boundaries according to the application's architecture.
- Validate on the server regardless of client-side validation.
- Use Zod or another established schema validator when appropriate.
- Prevent duplicate submissions where required.
- Provide clear pending, success, and failure states.
- Preserve form values after recoverable failures.
- Use optimistic updates only when rollback behavior is defined.
- Invalidate affected caches after successful mutations.
- Keep business workflows outside UI components.

---

## 12. TanStack Query and Client State

Do not use TanStack Query as a default replacement for Server Component data access.

Use it where client-managed server state provides meaningful value:

- Frequently refreshed data.
- Interactive dashboards.
- Client-driven pagination.
- Mutations and optimistic updates.
- Infinite scrolling.
- Data shared among multiple interactive components.
- Client-managed synchronization.

Rules:

- Use a consistent QueryClient configuration.
- Avoid accidental QueryClient recreation.
- Understand server/client cache hydration before implementing prefetching.
- Avoid leaking cached user-specific data between sessions.
- Invalidate or update affected queries after mutations.
- Avoid duplicating the same server state in Zustand.
- Use Zustand only for genuine client-global state.

---

## 13. Styling, Images, and Fonts

- Follow the companion `profiles/frontend/react.md` profile.
- Prefer Tailwind CSS where established by the project.
- Use the existing component library.
- Use Next.js-supported image optimization when appropriate.
- Configure remote image sources explicitly and narrowly.
- Avoid unnecessarily disabling image optimization.
- Use the framework's supported font optimization mechanisms where beneficial.
- Avoid layout shifts caused by images and fonts.
- Keep responsive design and accessibility requirements intact.

---

## 14. SEO and Metadata

For public-facing pages:

- Use the framework's supported metadata APIs.
- Define accurate titles and descriptions.
- Configure canonical URLs where appropriate.
- Provide Open Graph metadata where relevant.
- Configure robots directives intentionally.
- Generate sitemaps when useful.
- Use structured data only when accurate.
- Ensure public content is indexable when required.
- Prevent private or personalized content from being exposed through metadata or static output.

Do not prioritize SEO for private dashboards and internal tools where it has no meaningful value.

---

## 15. Security

Treat Next.js server and client boundaries as security boundaries.

Check for:

- Exposed server secrets.
- Unauthorized Server Actions.
- Insecure Route Handlers.
- IDOR.
- Tenant-isolation failures.
- XSS and unsafe HTML rendering.
- CSRF and unsafe cookie configuration.
- Open redirects.
- SSRF through user-controlled URLs.
- Unsafe file uploads.
- Cache poisoning and private-data cache leaks.
- Insecure webhook handling.
- Excessive request payloads.
- Dependency vulnerabilities.

Never use client-side rendering restrictions as a substitute for authorization.

---

## 16. Testing and Quality Gates

Preferred tools:

- Vitest or Jest.
- React Testing Library.
- Playwright.
- Framework-supported testing utilities appropriate to the installed version.

Test:

- Server and Client Component boundaries.
- Route navigation.
- Loading and error boundaries.
- Server Actions.
- Route Handlers.
- Authentication and authorization.
- Input validation.
- Cache invalidation.
- Data freshness.
- Hydration behavior.
- Critical user journeys.

Validation should include, where applicable:

```bash
npx tsc --noEmit
npx eslint .
npm run build
```

These are examples only. Use the repository's package manager and scripts instead of assuming npm or a particular command exists.

Do not claim validation succeeded unless the commands actually ran and passed.

---

## 17. Deployment and Runtime

- Inspect the target hosting environment before choosing deployment settings.
- Understand whether the deployment uses Node.js, Docker, a managed platform, or static export.
- Do not assume all Next.js features work with static export.
- Ensure Server Actions, Route Handlers, image optimization, and runtime-dependent functionality are supported by the chosen deployment model.
- Use production environment variables securely.
- Configure health checks and observability where appropriate.
- Use appropriate timeouts and resource limits.
- Avoid relying on local filesystem persistence in ephemeral serverless environments.
- Consider horizontal scaling and shared cache/session requirements.
- Use standalone output where appropriate for containerized deployment.
- Use multi-stage Docker builds and non-root runtime execution where practical.
- Keep build-time and runtime configuration requirements explicit.

---

## 18. Performance and Observability

Optimize based on measured or clearly identified bottlenecks.

Prioritize:

- Reducing unnecessary client JavaScript.
- Narrow Client Component boundaries.
- Appropriate rendering strategies.
- Cache correctness and invalidation.
- Avoiding request waterfalls.
- Parallelizing independent data access.
- Image and font optimization.
- Streaming where appropriate.
- Route-level code splitting.
- Monitoring Core Web Vitals.
- Structured server-side logging.
- Error monitoring and tracing where appropriate.

Do not introduce caching, streaming, or complex optimization mechanisms without a concrete reason.

---

## 19. Implementation Workflow

For substantial Next.js work:

1. Inspect `package.json`, lockfiles, and Next.js configuration.
2. Identify the installed Next.js and React versions.
3. Determine App Router or Pages Router.
4. Load `profiles/frontend/react.md` and this profile.
5. Identify Server and Client Component boundaries.
6. Establish data ownership and security boundaries.
7. Determine rendering and caching requirements.
8. Implement the smallest coherent solution.
9. Test authorization, error handling, and user-visible behavior.
10. Run type checks, linting, tests, and production build as appropriate.
11. Review for exposed secrets, hydration issues, unnecessary client bundles, and cache leaks.
12. Report changes and actual verification results.

---

## 20. Final Engineering Principles

- Prefer Server Components by default in App Router projects.
- Introduce Client Components only when interactivity requires them.
- Keep server-side data access on trusted boundaries.
- Treat Server Actions and Route Handlers as exposed entry points.
- Make rendering and caching decisions intentionally.
- Preserve backend ownership when an existing backend already exists.
- Keep the frontend architecture simple and maintainable.

**Final rule:** React standards govern component engineering. This profile governs Next.js-specific behavior. The installed framework version and repository configuration determine which APIs and conventions are valid.

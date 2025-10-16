# VISION: Codebase Integration Point Mapper

## Core Problem
Claude Code wastes cognitive cycles inferring "how does component A connect to component B?" Every code change requires understanding the full integration web—which functions call which, how data flows through the system, where modules intersect. Without a pre-computed integration map, Claude Code must parse, infer, and guess.

## Vision Statement
Create a Python AST analyzer that generates a **hierarchical integration map** showing EVERY crossroad, junction, and connection point between codebase components. The output is an industry-standard tree structure where Claude Code can instantly trace:
- "Show me every function that touches user authentication"
- "What's the complete data flow from API endpoint to database?"
- "Which components integrate with the payment module?"
- "Show me all crossroads where module A and module B interact"

## What This Is
An **integration point microscope** that reveals the connective tissue of your codebase:
- NOT a flat list of imports
- NOT a simple call graph
- YES a rich hierarchical tree showing HOW components integrate
- YES a flow map showing data/control paths through the system
- YES a junction catalog showing every crossroad between components

## What Makes This Different
**Previous approach:** Listed components → missed the integration points
**This approach:** Maps integration points → reveals the architecture

Every edge in the graph answers: "HOW do these components interact?"
- Function X calls Function Y **with what parameters?**
- Module A imports Module B **and uses which specific parts?**
- Class C inherits from Class D **and overrides which methods?**
- Data flows from Component E to Component F **through which path?**

## Success Vision
Claude Code loads the map and instantly sees:
```
"Show me integration points for user authentication"
→ Sees: 
  - auth.login() called by 12 endpoints
  - auth.validate_token() used by 8 middleware functions
  - User model imported by 15 modules
  - Data flow: request → validator → auth → database → response
  - Junction points: auth intersects with [api, models, middleware, utils]
```

## Developer Experience
You ask Claude Code: "Refactor payment processing"
- **Without map:** Claude searches files, infers connections, might miss edge cases
- **With map:** Claude sees payment module integration tree instantly, knows every touchpoint, plans refactor with zero guesswork

## Philosophical Core
**Integration > Isolation**
Components don't exist in vacuum—they exist in relationships. Map the relationships.

**Flow > Structure**
Static structure is useless—show how data/control FLOWS through components.

**Crossroads > Nodes**
Junction points where components meet are more important than the components themselves.

**Hierarchy > Flatness**
Tree structure mirrors how developers think: "This module contains these classes which have these methods which call these functions."

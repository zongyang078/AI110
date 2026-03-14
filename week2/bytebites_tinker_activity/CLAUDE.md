# ByteBites Design Agent

## Description
A focused agent for generating and refining ByteBites UML diagrams and scaffolds.

## Instructions

- This project is the ByteBites campus food ordering app backend.
- The system has exactly **4 classes**: Customer, MenuItem, Menu, Order.
- Do NOT add extra classes beyond these four.
- Do NOT introduce unnecessary complexity or features not in the spec.
- Always refer to `bytebites_spec.md` for the original feature request.

### Class Rules
- **Customer**: has name (str) and purchase_history (list). Can verify user.
- **MenuItem**: has name (str), price (float), category (str), popularity (float). No methods needed.
- **Menu**: holds a list of MenuItems. Supports add_item, filter_by_category, sort_by_popularity.
- **Order**: links to a Customer, holds a list of MenuItems. Supports add_item and calculate_total.

### Style
- Keep code simple and readable.
- Use type hints in Python.
- Follow the UML diagram in `draft_from_copilot.md`.
---
name: Broken Link Healer
description: Finds unresolved links, uses semantic context to guess the intended existing file, and corrects the link.
---

# Broken Link Healer Workflow

When the user uses the slash command `/heal_links` or asks to heal, format, or fix broken links in a specific file or folder, follow these steps:

1. **Find Broken Links**: Scan the text for `[[wikilinks]]` (or `[markdown](links)` if preferred) that point to files that **do not exist** in the repository/vault.
2. **Analyze Context**: For each broken link, extract the surrounding paragraph to understand the semantic context. Why might the link be broken?
   - Is it a plural/singular mismatch (e.g., `[[Apples]]` vs file `Apple`)?
   - Is there a typo (e.g., `[[Relatvity]]` vs file `Relativity`)?
   - Was a file renamed or moved but links weren't updated?
   - Did the user use a synonym instead of the true file name?
3. **Search for Matches**: Use your search tools against the current Vault directory to find existing files that are semantically similar, syntactically close, or aliases of the broken query.
4. **Propose Corrections**: 
   - Compile a list of broken links and their highly probable replacements.
   - If a link should be replaced dynamically preserving the text but pointing to the right file, propose an aliased link, e.g., changing `[[apples]]` to `[[Apple|apples]]`.
5. **Confirm and Apply Changes**: Show the proposed replacements to the user. Upon confirmation, update the target Markdown files, replacing the broken markdown syntax with the correct links.
6. **Notify**: Advise the user if any links appear truly orphaned (no suitable matching file exists and the note might need to be created from scratch).

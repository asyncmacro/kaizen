---
categories:
  - [[Series]]
type: series
title: "{{title}}"
year: {{year}}
genres: [{{genres}}]
network: "{{network}}"
status: "{{status}}"
rating: 
tmdb_id: "{{tmdbId}}"
total_seasons: {{totalSeasons}}
last_updated: <% tp.date.now("YYYY-MM-DD") %>
---

# {{title}}

> [!abstract] Overview
> ![[{{poster}}]]
> **Director/Creator:** {{director}}
> **Cast:** {{actors}}
> 
> {{plot}}

---

## 📺 Season Tracker
- [ ] Season 1
<%* if (parseInt("{{totalSeasons}}") > 1) { %>
- [ ] Season 2
<%* } %>

## 📝 My Notes
- 

---

## 🔗 Related Media
```dataview
LIST FROM #media/series 
WHERE contains(genres, this.genres[0]) AND file.name != this.file.name
LIMIT 5

---
cssClasses:
---

# 🏠 Command Center

> [!multi-column]
>
> > [!info]+ 📅 Today
> > **Date:** `= date(now)`
> > **Day:** `= dateformat(date(now), "cccc")`
> >
> > ### Quick Capture
> >
> > - [ ] Quick task
> > - [ ] Another thought
>
> > [!tip]+ 🎯 Focus Today
> >
> > #### Top 3 Priorities
> >
> > 1.
> > 2.
> > 3.
> >
> > _"What's the ONE thing I can do today?"_

---

## 📥 Inbox - Process These

```dataview
TABLE WITHOUT ID
  file.link as "📝 Note",
  dateformat(file.ctime, "MMM dd") as "Created"
FROM "000 - Inbox"
WHERE file.name != "Inbox"
SORT file.ctime DESC
LIMIT 8
```

---

> [!multi-column]
>
> > [!todo]+ ✅ Active Tasks
> >
> > ```dataview
> > TASK
> > FROM "500 - Projects" OR "400 - Areas"
> > WHERE !completed
> > LIMIT 10
> > ```
>
> > [!example]+ 🚀 Projects in Motion
> >
> > ```dataview
> > TABLE WITHOUT ID
> >   file.link as "Project",
> >   choice(status, status, "🟡 Active") as "Status"
> > FROM "500 - Projects"
> > WHERE file.name != "Projects"
> > SORT file.mtime DESC
> > LIMIT 5
> > ```

---

## 🧠 Recent Knowledge

> [!multi-column]
>
> > [!note]+ 📚 Latest Zettels
> >
> > ```dataview
> > LIST
> > FROM "300 - Zettelkasten"
> > SORT file.ctime DESC
> > LIMIT 6
> > ```
>
> > [!abstract]+ 📖 Sources to Process
> >
> > ```dataview
> > TABLE WITHOUT ID
> >   file.link as "Source",
> >   type as "Type"
> > FROM "200 - Source"
> > WHERE !processed
> > SORT file.ctime DESC
> > LIMIT 5
> > ```

---

## 🗺️ Quick Navigation

- #mcl/list-grid
  - ### 📥 [[000 - Inbox/Inbox|Capture Inbox]]
    - Quick notes & fleeting thoughts
  - ### 🗺️ [[100 - Map Of Contents|Maps of Content]]
    - Knowledge navigation hubs
  - ### 📖 [[200 - Source|Source Materials]]
    - Articles, videos, books
  - ### 🧠 [[300 - Zettelkasten|Zettelkasten]]
    - Atomic permanent notes
  - ### 🏡 [[400 - Areas|Life Areas]]
    - Ongoing responsibilities
  - ### 🚀 [[500 - Projects|Active Projects]]
    - Time-bound outcomes

---

_Last viewed: `= date(now)`_

# Roadmap HTML Visualization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create two distinct HTML visualizations (Dashboard and Infographic) for the End-to-End Roadmap.

**Architecture:** Single-file HTML solutions using modern CSS (Grid, Flexbox, Variables) and vanilla JS for interactivity.

**Tech Stack:** HTML5, CSS3 (CSS Variables, Glassmorphism, Ambient Shadows), JavaScript (Intersection Observer).

---

### Task 1: Dashboard Version Implementation

**Files:**
- Create: `raw/roadmap-dashboard.html`

- [ ] **Step 1: Scaffold HTML Structure**
Create the base HTML with a sidebar `<nav>` and a main `<article>` area.

- [ ] **Step 2: Implement Dashboard CSS (Layout & Post-processing)**
Apply the Dashboard style: fixed sidebar, scrollable content, and ambient light shadows.

```css
:root {
    --bg-color: #E4E4FF;
    --primary-color: #6260FF;
    --card-bg: rgba(255, 255, 255, 0.9);
    --shadow: 0 10px 30px rgba(98, 96, 255, 0.1);
}
body { background: var(--bg-color); display: flex; }
nav { width: 300px; position: fixed; height: 100vh; background: var(--primary-color); color: white; }
main { margin-left: 300px; padding: 40px; flex: 1; }
.card { background: var(--card-bg); border-radius: 16px; box-shadow: var(--shadow); margin-bottom: 24px; padding: 24px; backdrop-filter: blur(10px); }
```

- [ ] **Step 3: Map Content from Markdown**
Populate the HTML with content from `raw/Workflow_End_To_End_LoadMap.md`.

- [ ] **Step 4: Add Scroll Sync JS**
Implement Intersection Observer to highlight the active section in the sidebar.

- [ ] **Step 5: Verify & Commit**
Check the file in the browser (if possible) or verify structure.
```bash
git add raw/roadmap-dashboard.html
git commit -m "feat: add dashboard version of roadmap"
```

---

### Task 2: Infographic Version Implementation

**Files:**
- Create: `raw/roadmap-infographic.html`

- [ ] **Step 1: Scaffold Grid Structure**
Create a grid-based container for the infographic cards.

- [ ] **Step 2: Implement Infographic CSS (Ambient Glow & Cards)**
Apply the Bento-grid style with aggressive post-processing (hover glows).

```css
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 40px; }
.card { 
    background: white; 
    border-radius: 24px; 
    padding: 30px; 
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.card:hover { 
    transform: translateY(-5px); 
    box-shadow: 0 20px 40px rgba(98, 96, 255, 0.2); 
}
```

- [ ] **Step 3: Map Content & Add Visual Elements**
Populate cards with content and add prominent index numbers and icons.

- [ ] **Step 4: Implement Smooth Interactivity**
Add subtle entry animations for cards using CSS keyframes.

- [ ] **Step 5: Verify & Commit**
```bash
git add raw/roadmap-infographic.html
git commit -m "feat: add infographic version of roadmap"
```

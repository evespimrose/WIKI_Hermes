# Spec: Roadmap HTML Visualization (Dual Versions)

**Date**: 2026-06-11
**Topic**: Workflow End-to-End Roadmap HTML Generation
**Status**: Approved

## 1. Overview
Convert the `Workflow_End_To_End_LoadMap.md` content into two distinct HTML visualizations (Dashboard and Infographic) with modern UI/UX elements, focusing on visual clarity and a high-end feel.

## 2. Visual Requirements
- **Background Color**: `#E4E4FF` (Light Lavender)
- **Highlight Color**: `#6260FF` (Deep Indigo)
- **Post-Processing**: 
    - Card layouts with "Ambient Light" shadows (diffuse, soft glows).
    - Glassmorphism effects (subtle blur/transparency) where appropriate.
    - Transition animations for interaction.
- **Typography**: Modern sans-serif (Inter/Pretendard).

## 3. Architecture & Components

### 3.1 Version A: Dashboard Style (`roadmap-dashboard.html`)
- **Sidebar (Fixed)**: 
    - Left-side navigation.
    - Auto-highlighting active section based on scroll position.
    - Deep Indigo theme for the sidebar area.
- **Content Area (Scrolling)**:
    - White cards with soft purple glows.
    - Large typography for headers.
    - Dedicated styling for the "Mastermind Architecture Diagram".

### 3.2 Version B: Infographic Style (`roadmap-infographic.html`)
- **Grid Layout**: 
    - Bento-grid or multi-column card layout.
    - Each section (1-9) represented as a high-fidelity card.
- **Visual Cues**:
    - Prominent index numbers in `#6260FF`.
    - Icons for each section.
    - Hover effects that trigger "glow" post-processing (ambient light expansion).
- **Mastermind Diagram**: Centered or full-width card with high visual emphasis.

## 4. Technical Implementation
- **Framework**: Single-file HTML/CSS/JS (no external dependencies except Google Fonts).
- **Styling**: CSS Variables for colors, Flexbox/Grid for layout, CSS filters/shadows for post-processing.
- **Interactivity**: 
    - Intersection Observer for Dashboard sidebar sync.
    - Smooth scroll for navigation.
    - Hover animations for cards.

## 5. File Mapping
- **Source**: `d:\Fork\WIKI\raw\Workflow_End_To_End_LoadMap.md`
- **Output A**: `d:\Fork\WIKI\raw\roadmap-dashboard.html`
- **Output B**: `d:\Fork\WIKI\raw\roadmap-infographic.html`

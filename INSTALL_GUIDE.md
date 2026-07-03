# Fuchibol Cup 2026 - Circular Bracket Predictor

A highly-premium, state-of-the-art Flask application featuring an interactive circular knockout bracket predictor (inspired by Sport Bible's design) alongside a classic group stage scoreboard visualizer.

## Features
- **Circular Tournament Tree**: Dynamic, math-aligned SVG structure modeling the entire Round of 32 down to the Champion.
- **Interactive Predictor**: Click on any country flag to advance them to the next round with smooth glowing transitions and animations.
- **Visual Path Tracking**: Luminous, glowing line highlights tracing your chosen winner's path all the way to the center trophy.
- **Gold Confetti Celebration**: Crown your champion at the center trophy and experience a gorgeous particle explosion.
- **Group Stage View**: Beautifully structured grid showing real-time group match scoreboards.

## Getting Started

1. **Activate Environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Run Server**:
   ```bash
   python app.py
   ```

3. **Open Browser**:
   Navigate to **[http://127.0.0.1:5001](http://127.0.0.1:5001)**

## Static Compilation & Publishing (GitHub Pages)

The project includes a static compiler that produces a fully serverless site designed to run in `/docs` (configured for GitHub Pages deployment):

1. **Compile**:
   ```bash
   bash publish.sh
   ```
   This generates:
   - `docs/index.html` (with tournament scoreboard data fully inlined)
   - `docs/simulator.html` (with team, player, and head-to-head matches databases fully inlined)
   - `docs/holland_lop.jpg` (the custom local Netherlands logo replacement)
   - `docs/.nojekyll` (disables GitHub Pages' default Jekyll builds for fast assets)

2. **Deploy**:
   Commit the updated `/docs` directory and push to the remote branch:
   ```bash
   git add docs/
   git commit -m "Build and compile static tournament visualizer and simulator for GitHub Pages"
   git push origin main
   ```


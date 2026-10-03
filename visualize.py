"""Write an animated, self-contained HTML visualisation of A* vs Dijkstra.

Usage: python visualize.py [--rows 30] [--cols 50] [--seed 1] [--out pathfinding.html]
"""
import argparse
import json

from pathfinding import astar, dijkstra, make_grid

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Pathfinding: A* vs Dijkstra</title>
<style>
body{font-family:system-ui,sans-serif;background:#111;color:#eee;text-align:center;margin:1rem}
.row{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}
canvas{background:#1b1b1b;border:1px solid #333;max-width:100%}
button{padding:.4rem 1rem;margin:.5rem;border-radius:4px;border:0;cursor:pointer}
.legend span{display:inline-block;width:.9em;height:.9em;margin:0 .3em 0 1em;vertical-align:middle}
</style></head><body>
<h2>Pathfinding: A* vs Dijkstra</h2>
<p>Both find a shortest path; A*'s heuristic lets it explore far fewer cells.</p>
<div class="legend"><span style="background:#2e2e2e"></span>wall
<span style="background:#3b6fb6"></span>expanded<span style="background:#ffd23f"></span>path
<span style="background:#3ddc84"></span>start<span style="background:#ff4d4d"></span>goal</div>
<button id="replay">Replay</button>
<div class="row" id="panels"></div>
<script>
const DATA = __DATA__;
const CELL = Math.max(6, Math.min(16, Math.floor(560 / DATA.cols)));
const panels = document.getElementById("panels");
const runs = DATA.runs.map(run => {
  const box = document.createElement("div");
  const label = document.createElement("div");
  const cv = document.createElement("canvas");
  cv.width = DATA.cols * CELL; cv.height = DATA.rows * CELL;
  box.append(label, cv); panels.append(box);
  return {run, label, ctx: cv.getContext("2d")};
});
function rect(ctx, r, c, color){ctx.fillStyle = color; ctx.fillRect(c*CELL, r*CELL, CELL-1, CELL-1);}
function draw(p, step){
  const {run, ctx, label} = p;
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  DATA.grid.forEach((row, r) => row.forEach((v, c) => { if (v) rect(ctx, r, c, "#2e2e2e"); }));
  const n = Math.min(step, run.expanded.length);
  for (let i = 0; i < n; i++) rect(ctx, ...run.expanded[i], "#3b6fb6");
  const done = step >= run.expanded.length;
  if (done && run.path) run.path.forEach(([r, c]) => rect(ctx, r, c, "#ffd23f"));
  rect(ctx, ...DATA.start, "#3ddc84"); rect(ctx, ...DATA.goal, "#ff4d4d");
  label.textContent = run.name + " \\u2014 expanded " + n + "/" + run.expanded.length +
    (done ? (run.path ? ", path length " + (run.path.length - 1) : ", no path") : "");
}
let timer;
function play(){
  clearInterval(timer);
  const max = Math.max(...runs.map(p => p.run.expanded.length));
  const per = Math.max(1, Math.ceil(max / 300));
  let step = 0;
  timer = setInterval(() => {
    step += per; runs.forEach(p => draw(p, step));
    if (step >= max + per) clearInterval(timer);
  }, 25);
}
document.getElementById("replay").onclick = play;
play();
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=30)
    ap.add_argument("--cols", type=int, default=50)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default="pathfinding.html")
    a = ap.parse_args()

    grid = make_grid(a.rows, a.cols, seed=a.seed)
    start, goal = (0, 0), (a.rows - 1, a.cols - 1)
    runs = []
    for name, fn in (("A*", astar), ("Dijkstra", dijkstra)):
        path, expanded = fn(grid, start, goal)
        runs.append({"name": name, "path": path, "expanded": expanded})
        print(f"{name}: path={'none' if path is None else len(path) - 1} expanded={len(expanded)}")
    data = {"grid": grid, "rows": a.rows, "cols": a.cols, "start": start, "goal": goal, "runs": runs}
    with open(a.out, "w") as f:
        f.write(TEMPLATE.replace("__DATA__", json.dumps(data)))
    print("wrote", a.out)


if __name__ == "__main__":
    main()

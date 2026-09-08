import json, pathlib
from rtshield.benchmark import run_suite
out=run_suite(); pathlib.Path('results').mkdir(exist_ok=True); pathlib.Path('results/v0_1_benchmark.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))

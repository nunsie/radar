# Tech Radar

My opinions on languages, frameworks, tools, platforms and techniques, in the style of the
[Thoughtworks Technology Radar](https://www.thoughtworks.com/radar). These are my views in
my context, not universal verdicts.

**👉 [View the radar](https://radar.thoughtworks.com/?documentId=https%3A%2F%2Fraw.githubusercontent.com%2Fnunsie%2Fradar%2Frefs%2Fheads%2Fmain%2Fradar.csv)**

## Rings

- **Adopt** – my default choice; I'd use it without much debate.
- **Trial** – worth using on real work where the risk is manageable.
- **Assess** – worth exploring to understand how it could fit.
- **Hold** – proceed with caution; I'd avoid it for new work. (BYOR displays this as "Caution".)

## Adding or changing an entry

Create a Markdown file in the right quadrant folder under `quadrants/`:

```markdown
---
name: Kubernetes
ring: adopt        # adopt | trial | assess | hold
---
Why it's in this ring, when I'd avoid it, and what I'd use instead.
Markdown (bold, links, paragraphs) is converted to HTML for the radar.
```

Then regenerate the CSV and commit both:

```bash
pip install -r requirements.txt   # optional; a basic fallback is built in
python build.py          # writes radar.csv
python build.py --check  # validate only
```

Git history is the changelog: moving an entry between rings is just a commit.

### New and moved blips

`isNew` and the movement arrows are not authored by hand. `build.py` compares the
entries against the existing `radar.csv` and fills in BYOR's optional `status`
column:

- **New** – the name was not in the previous `radar.csv`.
- **Moved In** – the ring moved towards the centre (e.g. `assess` → `trial`).
- **Moved Out** – the ring moved towards the edge (e.g. `trial` → `assess`).
- **No Change** – same ring as before.

Because `radar.csv` is the baseline, the flags describe the change since the last
build and reset on the next one. Delete `radar.csv` to treat every entry as new.

CI rebuilds `radar.csv` automatically on every push to `main` that touches `quadrants/`,
`build.py` or `requirements.txt`, and commits the result. Pull requests run the validator
and fail if `radar.csv` is out of date.

## Viewing it in BYOR

1. Push the repo (it must be public).
2. Open the raw URL of `radar.csv`, e.g.
   `https://raw.githubusercontent.com/<you>/tech-radar/main/radar.csv`.
3. Paste that URL into [radar.thoughtworks.com](https://radar.thoughtworks.com).

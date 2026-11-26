# Fonts

The `fonts/` folder bundles the four DejaVu faces this entry's generator
uses: DejaVu Serif (regular + bold) for the masthead and headlines, and
DejaVu Sans (regular + bold) for kickers, labels and body copy.

DejaVu is free software, released under a permissive licence that allows
redistribution; the licence text is embedded in the font files
themselves. Bundling the files means `generate.py` never depends on whatever fonts happen to
be installed on the machine that draws the page — the same code draws
the same pixels everywhere.

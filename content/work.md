<!-- Each project: "## Title" then an optional "kick:" line, a "url:" line, and prose.
     The panel image is assets/<slug>.jpg if present, otherwise a generated placeholder. -->

## Fin-GloVe
kick: Word embeddings
url: #

General-purpose word vectors are trained on Wikipedia and news. They don't know that
"restatement" is ominous, or that "headwinds" is a hedge. Fin-GloVe is trained on financial
text instead, so the geometry reflects how the language is actually used in filings and disclosures.

Built for research use, with the corpus and vectors available for download.

## Novelty in finance research
kick: Interactive appendix · Review of Finance
url: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3803654

Which finance papers are genuinely new, and does novelty help or hurt publication? We measured
novelty and conventionality across the corpus of finance research, then built an appendix where
you can explore the results paper by paper rather than reading them off a table.

With Donohue, Drechsler, and Jiang. *Review of Finance*, 2023.

## Dealscan–Worldscope crosswalk
kick: Linking table · distributed on WRDS
url: https://wrds-web.wharton.upenn.edu/wrds/ds/wrdsapps/link/dswslink/index.cfm?navId=539

Loan-level data and international firm fundamentals don't share an identifier, which quietly
blocks a whole class of cross-border credit research. This crosswalk closes the gap.

Built for *International Lending: The Role of Lender's Home Country*, now maintained as a
standalone WRDS dataset.

## Form 10-Q itemization
kick: Text structuring
url: https://doi.org/10.1145/3459637.3481989

A 10-Q is a legally structured document that arrives as an unstructured blob. Getting from one
to the other reliably, across decades of inconsistent filings, is the unglamorous step that most
textual finance research depends on.

With Zhang, Du, Sun, and Donohue. ACM CIKM, 2021.

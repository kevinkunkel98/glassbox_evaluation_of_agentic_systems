#import "@preview/arkheion:0.1.2": arkheion, arkheion-appendices

#show: arkheion.with(
  title: "Automated Component-Level Evaluation of Software Engineering Agents",
  authors: (
    (
      name: "Kevin Kunkel",
      email: "mm21lugi@studserv.uni-leipzig.de",
      affiliation: "Faculty of Computer Science, University of Leipzig",
    ),
  ),
  // Insert your abstract after the colon, wrapped in brackets.
  // Example: `abstract: [This is my abstract...]`
  abstract: "Current evaluation of software engineering agents predominantly measures end-to-end task success, providing little insight into where and why agents fail. This work investigates whether individual agent steps can be reliably evaluated using LLM-based judges, without requiring human assessment of every decision. We collect trajectories from SWE-agent on SWE-bench instances and parse them into atomic steps, each characterized by the agent's reasoning, tool call, parameters, and observation. We manually annotate a subset of steps across three evaluation dimensions — tool selection, parameter quality, and step coherence — establishing a ground-truth dataset. Using this dataset, we design and systematically compare prompt variants (zero-shot, few-shot, chain-of-thought) for each dimension, measuring agreement between the LLM judge and human labels via accuracy and Cohen's kappa. Our analysis reveals which dimensions of agent behavior are amenable to automatic evaluation, where LLM judges fail systematically, and what this implies for the scalability of glass-box agent evaluation in software engineering contexts.",
  keywords: ("Glassbox", "Agentic", "Development", "LLMs"),
  date: "May 5, 2026",
)
#set cite(style: "chicago-author-date")
#show link: underline

= Introduction
#lorem(60)

= Heading: first level
#lorem(20)

== Heading: second level
#lorem(20)

=== Heading: third level

==== Paragraph
#lorem(20)

#lorem(20)

= Math

*Inline:* Let $a$, $b$, and $c$ be the side
lengths of right-angled triangle. Then, we know that: $a^2 + b^2 = c^2$

*Block without numbering:*

#math.equation(block: true, numbering: none, [
  $
    sum_(k=1)^n k = (n(n+1)) / 2
  $
])

*Block with numbering:*

As shown in @equation.

$
  sum_(k=1)^n k = (n(n+1)) / 2
$ <equation>

*More information:*
- #link("https://typst.app/docs/reference/math/equation/")


= Citation

You can use citations by using the `#cite` function with the key for the reference and adding a bibliography. Typst supports BibLateX and Hayagriva.

```typst
#bibliography("bibliography.bib")
```

Single citation @Vaswani2017AttentionIA. Multiple citations @Vaswani2017AttentionIA @hinton2015distilling. In text #cite(<Vaswani2017AttentionIA>, form: "prose")

*More information:*
- #link("https://typst.app/docs/reference/meta/bibliography/")
- #link("https://typst.app/docs/reference/meta/cite/")

= Figures and Tables


#figure(
  table(
    align: center,
    columns: (auto, auto),
    row-gutter: (2pt, auto),
    stroke: 0.5pt,
    inset: 5pt,
    [header 1], [header 2],
    [cell 1], [cell 2],
    [cell 3], [cell 4],
  ),
  caption: [#lorem(5)],
) <table>

#figure(
  image("image.png", width: 30%),
  caption: [#lorem(7)],
) <figure>

*More information*

- #link("https://typst.app/docs/reference/meta/figure/")
- #link("https://typst.app/docs/reference/layout/table/")

= Referencing

@figure #lorem(10), @table.

*More information:*

- #link("https://typst.app/docs/reference/meta/ref/")

= Lists

*Unordered list*

- #lorem(10)
- #lorem(8)

*Numbered list*

+ #lorem(10)
+ #lorem(8)
+ #lorem(12)

*More information:*
- #link("https://typst.app/docs/reference/layout/enum/")
- #link("https://typst.app/docs/reference/meta/cite/")


// Add bibliography and create Bibiliography section
#bibliography("bibliography.bib")

// Create appendix section
#show: arkheion-appendices
=

== Appendix section

#lorem(100)

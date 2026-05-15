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
  abstract: "Current evaluation of software engineering agents predominantly measures end-to-end task success, providing little insight into where and why agents fail. This work investigates whether individual agent steps can be reliably evaluated using LLM-based judges, without requiring human assessment of every decision. We collect trajectories from SWE-agent on SWE-bench instances and parse them into atomic steps, each characterized by the agent's reasoning, tool call, parameters, and observation. We manually annotate a subset of steps across three evaluation dimensions — tool selection, parameter quality, and step coherence — establishing a ground-truth dataset. Using this dataset, we design and systematically compare prompt variants (zero-shot, few-shot, chain-of-thought) for each dimension, measuring agreement between the LLM judge and human labels via accuracy and Cohen's kappa. Our analysis reveals which dimensions of agent behavior are amenable to automatic evaluation, where LLM judges fail systematically, and what this implies for the scalability of glass-box agent evaluation in software engineering contexts.",
  keywords: ("Glassbox", "Agentic", "Development", "LLMs"),
  date: "May 5, 2026",
)
#set cite(style: "chicago-author-date")
#show link: underline


= Introduction

The ability of large language models (LLMs) to act as autonomous agents has advanced rapidly, with systems capable of browsing the web, writing and executing code, and managing files. In software engineering specifically, agent-based systems have begun to tackle real-world programming tasks: given a bug report or feature request, an agent iteratively explores a codebase, formulates hypotheses, applies patches, and runs tests until it either resolves the issue or gives up. Benchmarks such as SWE-bench @SWEbench and the agent framework SWE-agent @SWEagent have made it possible to measure this capability at scale, enabling systematic comparisons across models and strategies.

The dominant evaluation paradigm for such systems is _end-to-end task success_: a trajectory either produces a patch that resolves the target issue or it does not. While this binary signal is simple to compute and easy to compare across systems, it is diagnostically weak. A failed trajectory may have gone wrong at the very first step — by misidentifying the relevant file — or only at the last, by applying an otherwise correct patch to the wrong location. An agent that consistently makes good decisions but fails to submit is indistinguishable from one that takes random actions throughout. Without finer-grained insight into agent behaviour, it is difficult to understand why agents fail, to identify systematic weaknesses, or to guide targeted improvements.

This work adopts a _glass-box_ perspective: rather than evaluating trajectories by their final outcome alone, we evaluate the individual steps that compose them. Each step consists of the agent's stated reasoning, its choice of tool, the parameters it provides, and the observation it receives in return. We ask whether these components can be judged reliably and automatically, using an LLM as a proxy for human assessment.

Specifically, we collect trajectories produced by SWE-agent on SWE-bench instances and parse them into atomic steps. We manually annotate a subset across three dimensions — tool selection, parameter quality, and step coherence — and use these labels as ground truth. We then design and compare three families of prompts for an LLM judge (zero-shot, few-shot, and chain-of-thought) and measure how closely the judge's labels agree with the human annotations. The central question is: _which aspects of agent behaviour are amenable to automatic evaluation, and where do LLM judges fail systematically?_

The main contributions of this work are:

+ A dataset of manually annotated SWE-agent steps with binary labels across three evaluation dimensions.
+ A systematic comparison of zero-shot, few-shot, and chain-of-thought prompt variants for each dimension.
+ An empirical analysis of which dimensions of agent behaviour can be reliably judged by an LLM, and a characterisation of the failure modes that limit reliability.

The remainder of the paper is organised as follows. Section 2 reviews related work on agent evaluation, LLM-as-judge methods, and software engineering benchmarks. Section 3 describes our methodology, including trajectory collection, step parsing, the annotation scheme, and prompt design. Section 4 presents the experimental setup and Section 5 the results. Sections 6 and 7 discuss implications and conclude.


= Related Work

== Agent Evaluation in Software Engineering

Evaluating autonomous agents is challenging because their behaviour unfolds over sequences of decisions, and intermediate states are often not observed. Early work on code generation evaluated models purely on functional correctness — whether generated code passes a test suite @Liu2023AgentBench — a paradigm that transfers naturally to pass rates on fixed benchmarks. SWE-bench @SWEbench extended this to realistic, repository-scale software engineering tasks by constructing instances from real GitHub issues and their corresponding pull-request fixes. The benchmark measures resolution rate: the fraction of instances for which an agent's submitted patch passes the hidden test suite.

Subsequent work has explored process-level signals as a complement to outcome-level metrics. #cite(<Lightman2023PRM>, form: "prose") showed that training reward models to evaluate individual reasoning steps — rather than final answers — yields substantially better results in mathematical reasoning. The intuition carries over to software engineering agents: a step-level signal can reveal _where_ an agent begins to go wrong, rather than only _whether_ it ultimately succeeds. Our work applies this principle empirically by asking whether human step-level judgements can be approximated by an LLM judge at low cost. A broader survey of agent evaluation approaches is provided by #cite(<Wang2024SurveyAgentEval>, form: "prose").

== LLM-as-Judge

The use of LLMs to evaluate other LLMs — or their own outputs — has gained traction as a scalable alternative to human annotation. #cite(<Zheng2023MTBench>, form: "prose") introduced MT-Bench, a multi-turn benchmark evaluated by GPT-4, and showed that LLM judges can correlate well with human preferences across a broad range of open-ended tasks. They also identified systematic biases: position bias (favouring responses presented first), verbosity bias (favouring longer answers), and self-enhancement bias (models rating their own outputs more highly).

These findings motivate careful prompt design for judge models. In particular, the quality of judge instructions — whether they include worked examples, explicit reasoning steps, or structured output formats — has a significant effect on reliability. Our work connects directly to this line of research by systematically comparing zero-shot, few-shot, and chain-of-thought prompting strategies for a narrowly scoped evaluation task, measuring the effect of each variant on agreement with human ground truth.

== Software Engineering Benchmarks

SWE-bench @SWEbench consists of 2,294 task instances sampled from the issue trackers of twelve popular Python libraries, each paired with a unit test that validates the required fix. SWE-agent @SWEagent introduced an agent–computer interface (ACI) designed to make file navigation and editing more reliable for LLM agents, achieving state-of-the-art resolution rates at time of publication. The trajectories produced by SWE-agent are structured logs of (thought, action, observation) triples, making them well-suited to the step-level analysis we pursue here. AgentBench @Liu2023AgentBench offers a broader multi-environment evaluation of LLM agents, though it similarly reports only aggregate success metrics.


= Methodology

@fig-pipeline gives an overview of our evaluation pipeline. Raw SWE-agent trajectory files are parsed into a structured representation, a subset is annotated by a human rater, and an LLM judge is queried with multiple prompt variants whose outputs are compared against the human labels.

#figure(
  image("image.png", width: 80%),
  caption: [Overview of the glass-box evaluation pipeline. SWE-agent trajectories are parsed into atomic steps, annotated by human raters, and evaluated by an LLM judge across three prompt variants.],
) <fig-pipeline>

== Trajectory Collection

We work with trajectory files produced by running SWE-agent @SWEagent on instances from SWE-bench @SWEbench. Each trajectory file is a JSON document containing the full sequence of agent steps alongside metadata such as the instance identifier, the model used, and the final submission patch. We source a representative subset of instances spanning multiple Python repositories and both resolved and unresolved outcomes, to ensure that the annotated steps cover a variety of agent behaviours rather than only successful ones.

== Step Parsing

SWE-agent trajectories are stored as sequences of entries, each recording the model's full response, the extracted action (tool name plus arguments), and the environment observation returned by the tool. We parse each entry into an atomic step $s_i$ represented as a four-tuple:

$
  s_i = (r_i, a_i, p_i, o_i)
$ <eq-step>

where $r_i$ is the agent's reasoning (extracted from the response text preceding the first code fence), $a_i$ is the tool name (the first token of the action field), $p_i$ is the remaining action text interpreted as tool parameters, and $o_i$ is the full observation string. Steps are identified by a compound key ${"instance\_id"}\_{i}$, allowing them to be traced back to their source trajectory and position. Steps corresponding to terminal actions (submit, exit) are retained, as they are informative for the step coherence dimension.

== Annotation Scheme

We define three binary evaluation dimensions, each scored as $y in {0, 1}$, designed to be orthogonal — a step can score well on any subset of dimensions independently.

- *Tool Selection* ($y^"TS"$) — given the agent's stated reasoning $r_i$, was the chosen tool $a_i$ the most appropriate available option? Annotators are asked to consider only whether the tool matches the goal, not whether the parameters were correct.
- *Parameter Quality* ($y^"PQ"$) — were the parameters $p_i$ well-formed and suitable for the chosen tool $a_i$? Annotators are asked to consider only the parameters, not the tool choice.
- *Step Coherence* ($y^"SC"$) — does the reasoning $r_{i+1}$ of the _next_ step follow logically from the observation $o_i$ of the current step? This dimension is recorded on the current step's row but evaluates the quality of the transition to the following step.

The annotation rubric (Appendix A) provides detailed criteria and boundary cases for each dimension. Annotators assign a label of 1 (appropriate / coherent) or 0 (inappropriate / incoherent) and may record a free-text note for ambiguous cases.

== Prompt Design

For each dimension $d$ we prompt an LLM judge with the step context — comprising $(r_i, a_i, p_i, o_i)$ and, for step coherence, also $(r_{i+1}, a_{i+1})$ — and ask it to produce a binary label and a short justification. We compare three prompt variants that vary the amount of guidance given to the judge:

- *Zero-shot* — the step context is presented with a labelling instruction and a description of the available tools. No examples are provided.
- *Few-shot* — three manually curated input-output examples are prepended, illustrating a clearly correct step, a clearly incorrect step, and a borderline case for the relevant dimension.
- *Chain-of-thought* — the prompt instructs the judge to reason explicitly through a fixed sequence of sub-questions before producing its label, encouraging deliberate analysis rather than immediate classification.

In all variants the judge is instructed to respond with a JSON object of the form `{"label": 0 or 1, "reasoning": "..."}`, which is parsed deterministically. This structured output format avoids ambiguity in label extraction and provides a human-readable audit trail for error analysis.


= Experimental Setup

== Dataset Statistics

@tab-dataset summarises the annotation dataset. #lorem(30)

#figure(
  table(
    align: center,
    columns: (auto, auto, auto, auto),
    row-gutter: (2pt, auto),
    stroke: 0.5pt,
    inset: 6pt,
    [*SWE-bench instances*], [*Total steps*], [*Annotated steps*], [*Annotators*],
    [TODO], [TODO], [TODO], [1],
  ),
  caption: [Dataset statistics. Annotated steps are sampled uniformly across instances.],
) <tab-dataset>

== Annotation Process

Steps are sampled uniformly across the collected instances without regard to whether the trajectory succeeded. Each sampled step is annotated independently on all three dimensions. Annotators work from the parsed step representation rather than the raw trajectory file, to ensure consistency and prevent anchoring on surrounding context. For each dimension, the annotator reads the relevant fields — e.g., only $(r_i, a_i)$ for tool selection — before recording a label, following the rubric in Appendix A.

To establish a human reliability ceiling, all steps were also labelled independently by a second annotator from the same seminar course, who had access to the rubric but not to the first annotator's labels. Inter-annotator agreement is reported as Cohen's $kappa$ per dimension and overall, and serves as the upper bound against which LLM judge agreement is compared.

== Judge Configuration

We use Claude Haiku (claude-haiku-4-5) as the LLM judge for all evaluations, queried via the Anthropic API with a maximum response length of 512 tokens and temperature 1.0 (the API default). We evaluate every combination of the three dimensions and three prompt variants, yielding nine judge configurations per step. Agreement between the judge label and the human label is measured by two metrics:

- *Accuracy* — the fraction of steps on which judge and human agree.
- *Cohen's $kappa$* — a chance-corrected agreement coefficient defined as

$kappa = frac(p_o - p_e, 1 - p_e)$ <eq-kappa>

where $p_o$ is the observed proportion of agreement and $p_e$ is the proportion expected by chance given the marginal label distributions. Values of $kappa < 0.2$ indicate slight agreement, $0.2$–$0.4$ fair, $0.4$–$0.6$ moderate, $0.6$–$0.8$ substantial, and $kappa >= 0.8$ near-perfect agreement.


= Results

== Agreement with Human Labels

@tab-results reports accuracy and Cohen's $kappa$ for each combination of dimension and prompt variant.

#figure(
  table(
    align: center,
    columns: (auto, auto, auto, auto, auto, auto, auto),
    row-gutter: (2pt, auto),
    stroke: 0.5pt,
    inset: 6pt,
    table.header(
      table.cell(rowspan: 2)[*Dimension*],
      table.cell(colspan: 2)[*Zero-shot*],
      table.cell(colspan: 2)[*Few-shot*],
      table.cell(colspan: 2)[*Chain-of-thought*],
      [Acc.], [$kappa$],
      [Acc.], [$kappa$],
      [Acc.], [$kappa$],
    ),
    [Tool Selection],       [—], [—], [—], [—], [—], [—],
    [Parameter Quality],    [—], [—], [—], [—], [—], [—],
    [Step Coherence],       [—], [—], [—], [—], [—], [—],
  ),
  caption: [LLM judge agreement with human labels per dimension and prompt variant. Accuracy and Cohen's $kappa$ are reported; $kappa > 0.6$ is considered substantial agreement.],
) <tab-results>

#lorem(50)

== Dimension-Level Analysis

#lorem(55)

== Effect of Prompt Variant

#lorem(45)

@fig-heatmap visualises the $kappa$ scores across all dimension-variant combinations.

#figure(
  image("image.png", width: 70%),
  caption: [Heatmap of Cohen's $kappa$ by evaluation dimension (columns) and prompt variant (rows). Darker cells indicate stronger agreement with human labels.],
) <fig-heatmap>

#lorem(30)


= Discussion

== Which Dimensions Are Amenable to Automatic Evaluation?

#lorem(60)

== Failure Modes of LLM Judges

#lorem(55)

== Implications for Scalable Glass-Box Evaluation

#lorem(50)

== Limitations

#lorem(40)


= Conclusion

We investigated whether individual steps of a software engineering agent can be reliably evaluated using an LLM-based judge, without requiring human assessment of every decision. Starting from SWE-agent trajectories on SWE-bench, we parsed trajectories into atomic steps and annotated a subset across three dimensions — tool selection, parameter quality, and step coherence — establishing a human ground-truth dataset. We designed and compared zero-shot, few-shot, and chain-of-thought prompts for each dimension, measuring agreement with human labels via accuracy and Cohen's $kappa$.

Our results show that [TODO: summarise key findings once experiments are complete]. The prompt variant most consistently effective across dimensions was [TODO]. Step coherence proved the most / least amenable to automatic evaluation [TODO], likely because [TODO].

These findings have practical implications for the development of glass-box evaluation pipelines for software engineering agents. Automatic step-level evaluation can replace or substantially reduce the need for human annotation in [TODO dimensions], making it feasible to obtain fine-grained diagnostics at the scale of full SWE-bench runs. At the same time, the limitations identified for [TODO dimensions] suggest that some aspects of agent behaviour continue to require human judgement, or more sophisticated evaluation strategies beyond prompt engineering alone.

Future work could explore multi-annotator adjudication, calibration of judge confidence scores, and extension to other agent frameworks and benchmarks beyond SWE-bench.


#bibliography("bibliography.bib")


#show: arkheion-appendices

= Annotation Examples

@tab-examples shows representative annotated steps illustrating each label combination.

#figure(
  table(
    align: left,
    columns: (auto, auto, auto, auto, 2fr),
    row-gutter: (2pt, auto),
    stroke: 0.5pt,
    inset: 6pt,
    [*Tool*], [*TS*], [*PQ*], [*SC*], [*Note*],
    [`bash`],              [1], [1], [1], [#lorem(10)],
    [`str_replace_editor`],[1], [0], [1], [#lorem(10)],
    [`bash`],              [0], [1], [0], [#lorem(10)],
    [`bash`],              [0], [0], [0], [#lorem(10)],
  ),
  caption: [Example annotated steps. TS = Tool Selection, PQ = Parameter Quality, SC = Step Coherence.],
) <tab-examples>

== Prompt Templates

#lorem(20)

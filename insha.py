import os
import json
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Make sure .env is in this folder and formatted correctly.")

client = OpenAI(api_key=api_key)



#JSON SCHema
STRUCTURED_PEE_ESSAY_SCHEMA: Dict[str, Any] = {
    "name": "structured_pee_essay",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "topic",
            "question",
            "audience",
            "citation_style",
            "introduction",
            "body",
            "conclusion",
            "sources",
            "web_research_log",
            "latex",
            "quality_checks"
        ],
        "properties": {
            "topic": {"type": "string"},
            "question": {"type": "string"},
            "audience": {"type": "string"},
            "citation_style": {"type": "string", "enum": ["apa", "mla"]},

            "introduction": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "hook",
                    "transition_after_hook",
                    "background",
                    "transition_to_thesis",
                    "thesis"
                ],
                "properties": {
                    "hook": {"type": "string"},
                    "transition_after_hook": {"type": "string"},
                    "background": {"type": "string"},
                    "transition_to_thesis": {"type": "string"},
                    "thesis": {"type": "string"}
                }
            },

            "body": {
                "type": "object",
                "additionalProperties": False,
                "required": ["paragraph_count", "paragraphs"],
                "properties": {
                    "paragraph_count": {"type": "integer", "minimum": 1},
                    "paragraphs": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            # NOTE: validator requires ALL properties to be listed in required
                            "required": [
                                "heading",
                                "point",
                                "evidence",
                                "explanation",
                                "link_back_to_question",
                                "cohesion",
                                "user_supplied_text",
                                "constraints"
                            ],
                            "properties": {
                                "heading": {"type": "string"},
                                "point": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    # NOTE: list both keys as required (allow empty string for user_supplied_fragment)
                                    "required": ["text", "user_supplied_fragment"],
                                    "properties": {
                                        "text": {"type": "string"},
                                        "user_supplied_fragment": {"type": "string", "description": "May be empty if user didn't provide a fragment."}
                                    }
                                },
                                "evidence": {
                                    "type": "array",
                                    "minItems": 1,
                                    "items": {
                                        "type": "object",
                                        "additionalProperties": False,
                                        "required": ["kind", "content", "source_id", "in_text_citation"],
                                        "properties": {
                                            "kind": {"type": "string", "enum": ["quote", "paraphrase", "data"]},
                                            "content": {"type": "string"},
                                            "source_id": {"type": "string"},
                                            "in_text_citation": {"type": "string"}
                                        }
                                    }
                                },
                                "explanation": {"type": "string"},
                                "link_back_to_question": {"type": "string"},
                                "cohesion": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "required": ["transition_from_previous", "transition_to_next"],
                                    "properties": {
                                        "transition_from_previous": {"type": "string"},
                                        "transition_to_next": {"type": "string"}
                                    }
                                },
                                # These two are now "required" by validator; allow empty defaults
                                "user_supplied_text": {"type": "string", "description": "May be empty if not provided."},
                                "constraints": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "required": ["must_include_terms", "prohibited_terms"],
                                    "properties": {
                                        "must_include_terms": {"type": "array", "items": {"type": "string"}},
                                        "prohibited_terms": {"type": "array", "items": {"type": "string"}}
                                    }
                                }
                            }
                        }
                    }
                }
            },

            "conclusion": {
                "type": "object",
                "additionalProperties": False,
                "required": ["synthesis", "restated_thesis", "final_takeaway"],
                "properties": {
                    "synthesis": {"type": "string"},
                    "restated_thesis": {"type": "string"},
                    "final_takeaway": {"type": "string"}
                }
            },

            "sources": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    # NOTE: include ALL properties in required; allow empty strings when unknown
                    "required": [
                        "id",
                        "kind",
                        "title",
                        "url",
                        "accessed",
                        "authors",
                        "year",
                        "publisher_or_site",
                        "container",
                        "pages",
                        "doi_or_identifier",
                        "formatted_reference"
                    ],
                    "properties": {
                        "id": {"type": "string"},
                        "kind": {
                            "type": "string",
                            "enum": ["web", "book", "journal", "report", "newspaper", "magazine", "video", "dataset"]
                        },
                        "title": {"type": "string"},
                        "url": {"type": "string"},
                        "accessed": {"type": "string"},
                        "authors": {"type": "array", "items": {"type": "string"}},
                        "year": {"type": "string"},
                        "publisher_or_site": {"type": "string"},
                        "container": {"type": "string", "description": "May be empty if N/A."},
                        "pages": {"type": "string", "description": "May be empty if N/A."},
                        "doi_or_identifier": {"type": "string", "description": "May be empty if N/A."},
                        "formatted_reference": {"type": "string"}
                    }
                }
            },

            "web_research_log": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["query", "rationale", "top_results"],
                    "properties": {
                        "query": {"type": "string"},
                        "rationale": {"type": "string"},
                        "top_results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["title", "url"],
                                "properties": {
                                    "title": {"type": "string"},
                                    "url": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            },

            "latex": {"type": "string"},

            "quality_checks": {
                "type": "object",
                "additionalProperties": False,
                # NOTE: include 'notes' in required to satisfy validator; allow empty string
                "required": [
                    "all_in_text_citations_match_sources",
                    "no_orphan_sources",
                    "pee_structure_verified",
                    "links_back_to_question_present",
                    "notes"
                ],
                "properties": {
                    "all_in_text_citations_match_sources": {"type": "boolean"},
                    "no_orphan_sources": {"type": "boolean"},
                    "pee_structure_verified": {"type": "boolean"},
                    "links_back_to_question_present": {"type": "boolean"},
                    "notes": {"type": "string", "description": "May be empty."}
                }
            }
        }
    }
}

#LATEX RENDER
def render_latex(doc: dict) -> str:
    title = doc["topic"]
    author = "Generated Essay"
    citation_style = doc.get("citation_style", "apa")

    intro = doc["introduction"]
    body = doc["body"]
    concl = doc["conclusion"]
    sources = doc["sources"]

    def latex_escape(s: str) -> str:
        repl = {
            "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
            "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}", "\\": r"\textbackslash{}"
        }
        for k, v in repl.items():
            s = s.replace(k, v)
        return s

    # Bibliography
    bib_items = []
    for src in sources:
        bib_items.append(
            f"\\bibitem{{{latex_escape(src['id'])}}} {latex_escape(src['formatted_reference'])}"
        )

    # Body
    body_blocks = []
    for i, p in enumerate(body["paragraphs"], start=1):
      
        heading = p.get("heading") or ""
        heading_line = latex_escape(heading) + ("\n\n" if heading else "")

        # Build a single flowing paragraph:
        pieces = []

        # Transition from previous, if any
        tprev = p["cohesion"].get("transition_from_previous", "").strip()
        if tprev:
            pieces.append(tprev.rstrip(".") + ".")  # ensure sentence closure

        # Point sentence
        point_txt = p["point"].get("user_supplied_fragment") or p["point"]["text"]
        if point_txt:
            pieces.append(point_txt.rstrip(".") + ".")

        # Evidence sentences (
        ev_sentences = []
        for ev in p["evidence"]:
            ev_sentences.append(f"{ev['content']} ({ev['in_text_citation']}).")
        if ev_sentences:
            pieces.append(" ".join(ev_sentences))

        # Explanation/analysis
        explain = p["explanation"].strip()
        if explain:
            pieces.append(explain.rstrip(".") + ".")

        # Link back to question
        linkback = p["link_back_to_question"].strip()
        if linkback:
            pieces.append(linkback.rstrip(".") + ".")

        # Transition to next, if any (we’ll append at the end)
        tnext = p["cohesion"].get("transition_to_next", "").strip()
        if tnext:
            pieces.append(tnext.rstrip(".") + ".")

        paragraph_text = latex_escape(" ".join(pieces))
        body_blocks.append(heading_line + paragraph_text)

    intro_block = "\n".join([
        "\\section*{Introduction}",
        latex_escape(intro["hook"]),
        latex_escape(intro.get("transition_after_hook", "")),
        latex_escape(intro["background"]),
        latex_escape(intro.get("transition_to_thesis", "")),
        "\\textbf{Thesis:} " + latex_escape(intro["thesis"])
    ])

    concl_block = "\n".join([
        "\\section*{Conclusion}",
        latex_escape(concl["synthesis"]),
        "\\\\[0.25em]" + latex_escape(concl["restated_thesis"]),
        "\\\\[0.25em]" + latex_escape(concl["final_takeaway"])
    ])

    body_text = "\n\n".join(body_blocks)
    refs_text = "\n".join(bib_items)

    document = f"""\\documentclass[12pt]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{hyperref}}
\\usepackage{{setspace}}
\\usepackage{{parskip}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{lmodern}}
\\usepackage{{enumitem}}

\\title{{{latex_escape(title)}}}
\\author{{{latex_escape(author)}}}
\\date{{}}

\\begin{{document}}
\\maketitle
\\onehalfspacing

{intro_block}

\\section*{{Body}}
{body_text}

{concl_block}

\\section*{{References ({citation_style.upper()})}}
\\begin{{thebibliography}}{{99}}
{refs_text}
\\end{{thebibliography}}

\\end{{document}}
"""
    return document

# Instruction Builder
def build_user_instruction(
    topic: str,
    question: str,
    audience: str = "General academic reader",
    citation_style: Optional[str] = None,
    paragraph_count: Optional[int] = None,
    paragraph_specs: Optional[List[Dict[str, Any]]] = None,
    user_intro_overrides: Optional[Dict[str, str]] = None,
) -> str:
    lines = [
        f"TOPIC: {topic}",
        f"QUESTION: {question}",
        f"AUDIENCE: {audience}",
        f"CITATION_STYLE (default APA): {citation_style or 'apa'}",
        "REQUIREMENTS:",
        "- Use PEE paragraphs (Point, Evidence, Explain) with an explicit link back to the question.",
        "- Write each body paragraph as a SINGLE, FLOWING piece of prose.",
        "- Do NOT include labels like 'Point:', 'Evidence:', 'Explain:', or 'Link:'.",
        "- Do NOT use bold or other styling markers inside the paragraph text.",
        "- ALWAYS use web search to support claims; include at least 2 credible sources.",
        "- Evidence must include correct APA/MLA in-text citations and a formatted reference list.",
        "- If user provides fragments, include them verbatim and complete the rest.",
        "- Respect desired paragraph count exactly if provided; else default to 3.",
        "- Introduction format: Hook → (transition) → Background → (transition) → Thesis.",
        "- Ensure quality checks are true; otherwise revise before finalizing.",
    ]
    if paragraph_count:
        lines.append(f"BODY_PARAGRAPH_COUNT: {paragraph_count}")
    if paragraph_specs:
        lines.append("PARAGRAPH_SPECS (apply in order; fill missing fields):")
        for i, spec in enumerate(paragraph_specs, 1):
            lines.append(f"  - P{i}: {json.dumps(spec, ensure_ascii=False)}")
    if user_intro_overrides:
        lines.append("INTRO_OVERRIDES (optional): " + json.dumps(user_intro_overrides, ensure_ascii=False))
    return "\n".join(lines)


# Response API calls
def generate_essay_json(
    topic: str,
    question: str,
    audience: str = "General academic reader",
    citation_style: Optional[str] = None,
    paragraph_count: Optional[int] = None,
    paragraph_specs: Optional[List[Dict[str, Any]]] = None,
    user_intro_overrides: Optional[Dict[str, str]] = None,
    model: str = "gpt-5"
) -> Dict[str, Any]:
    system_rules = (
        "You write essays in EXACTLY the schema provided via text.format.json_schema. "
        "Always perform web research using the web_search tool to support claims with citations. "
        "If the user does not specify a citation style, default to APA. "
        "Preserve any user-supplied fragments verbatim. "
        "Ensure PEE/PEEL structure per paragraph and link each paragraph back to the guiding question. "
        "Output ONLY content that validates against the schema."
    )

    user_instruction = build_user_instruction(
        topic=topic,
        question=question,
        audience=audience,
        citation_style=citation_style,
        paragraph_count=paragraph_count,
        paragraph_specs=paragraph_specs,
        user_intro_overrides=user_intro_overrides
    )

    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_rules},
            {"role": "user", "content": user_instruction}
        ],
        tools=[{"type": "web_search"}],
   extra_body={
    "text": {
        "format": {
            "name": "structured_pee_essay",
            "type": "json_schema",
            "schema": STRUCTURED_PEE_ESSAY_SCHEMA["schema"] # schema not json schema
        }
    }
}

    )

   
    if hasattr(resp, "output_parsed") and resp.output_parsed is not None:
        return resp.output_parsed  # type: ignore[attr-defined]

    # Fallbacks: collect text and json.loads
    raw_text = ""
    if hasattr(resp, "output_text") and isinstance(resp.output_text, str):
        raw_text = resp.output_text.strip()

    if not raw_text and hasattr(resp, "output"):
        try:
            chunks = []
            for item in getattr(resp, "output", []):
                for c in getattr(item, "content", []):
                    # newer SDKs: type could be "output_text" or "text"
                    t = getattr(c, "type", "")
                    if t in ("output_text", "text") and hasattr(c, "text"):
                        chunks.append(c.text)
            raw_text = "".join(chunks).strip()
        except Exception:
            pass

    if not raw_text:
        raise RuntimeError("No parseable text found in Responses API result.")

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        preview = raw_text[:800]
        raise RuntimeError(f"Model did not return valid JSON (first 800 chars):\n{preview}") from e

#Quality Check
def validate_quality(doc: Dict[str, Any]) -> None:
    qc = doc.get("quality_checks", {})
    problems = []
    if not qc.get("all_in_text_citations_match_sources", False):
        problems.append("Some in-text citations do not match 'sources'.")
    if not qc.get("no_orphan_sources", False):
        problems.append("Some sources are not cited in-text.")
    if not qc.get("pee_structure_verified", False):
        problems.append("One or more paragraphs lack proper PEE structure.")
    if not qc.get("links_back_to_question_present", False):
        problems.append("Missing link-back-to-question sentences.")
    if problems:
        raise AssertionError("Quality checks failed:\n- " + "\n- ".join(problems))


if __name__ == "__main__":
  
    topic = input("Enter the essay topic/title: ").strip()
    question = input("Enter the guiding question/prompt (or press Enter to reuse the topic): ").strip()
    if not question:
        question = topic

    # Body paragraph count (must be >=1)
    while True:
        try:
            paragraph_count = int(input("How many body paragraphs? ").strip())
            if paragraph_count >= 1:
                break
            print("Please enter an integer >= 1.")
        except ValueError:
            print("Please enter a valid integer.")

 
    citation_style_in = input("Citation style (apa|mla, default apa): ").strip().lower()
    citation_style = citation_style_in if citation_style_in in {"apa", "mla"} else "apa"

  
    normalized_specs: List[Dict[str, Any]] = []

    # --- Generate ---
    doc = generate_essay_json(
        topic=topic,
        question=question,
        audience="General academic reader",
        citation_style=citation_style,
        paragraph_count=paragraph_count,
        paragraph_specs=normalized_specs,
        user_intro_overrides=None,
        model="gpt-5"
    )

  
    try:
        validate_quality(doc)
    except AssertionError as err:
        print("Quality validation warning:\n", err)

    # Render LAtex and save
    tex = render_latex(doc)
    with open("essay.tex", "w", encoding="utf-8") as f:
        f.write(tex)
    with open("essay.json", "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

    print("Done. Wrote essay.tex and essay.json")

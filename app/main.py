from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Incident
from .schemas import IncidentRequest, IncidentResponse
from .prompt import build_prompt
from .llm import call_llm
from app.retrieval import retrieve_similar_cases


app = FastAPI(title="Root Cause Analyzer API")

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
def analyze_incident(request: IncidentRequest, db: Session = Depends(get_db)):
    incident_text = request.incident_text

    similar_cases = retrieve_similar_cases(incident_text)

    examples = ""
    for case in similar_cases:
        examples += f"""
Incident: {case['incident']}
Root Cause: {case['root_cause']}
Resolution: {case['resolution']}
"""

    prompt = f"""
You are an IT root cause analysis assistant.

Use step-by-step reasoning.

Follow these steps:
1. Identify affected services.
2. Correlate log anomalies.
3. Infer probable root cause.

Here are similar past incidents:
{examples}

Now analyze this incident:
{incident_text}

Respond strictly in JSON:
{{
  "steps": [],
  "root_cause": "",
  "resolution": ""
}}
"""

    result = call_llm(prompt)

    # Normalize the LLM response into a friendly analysis string
    analysis_parts = []
    if isinstance(result, dict):
        steps = result.get("steps") or []
        if steps:
            analysis_parts.append("Steps:\n" + "\n".join(f"- {s}" for s in steps))

        root = result.get("root_cause") or result.get("rootCause") or ""
        if root:
            analysis_parts.append(f"Root Cause: {root}")

        resolution = result.get("resolution") or ""
        if resolution:
            analysis_parts.append(f"Resolution: {resolution}")
    else:
        # If LLM returned a plain string, include it as-is
        analysis_parts.append(str(result))

    analysis_text = "\n\n".join(analysis_parts).strip()

    # Return a payload the frontend expects: `analysis` and `similar_cases`.
    return {
        "analysis": analysis_text,
        "similar_cases": similar_cases,
        # include raw llm result for additional debugging/consumption
        "raw": result,
    }



@app.options("/analyze")
def analyze_options():
    return Response(status_code=200)


@app.get("/incidents")
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).all()

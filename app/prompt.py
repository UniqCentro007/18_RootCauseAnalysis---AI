def build_prompt(incident: str) -> str:
    return f"""
You are an IT root cause analysis assistant.

Analyze the following incident step by step.

Incident:
{incident}

Steps:
1. Identify affected service.
2. Analyze log anomalies.
3. Infer probable root cause.
4. Suggest mitigation.

Respond strictly in JSON format:

{{
  "steps": ["step1", "step2", "step3"],
  "root_cause": "text",
  "resolution": "text"
}}
"""

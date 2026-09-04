def create_prompt(detections):
    return f"""
You are an expert Solar Panel Inspection AI.

YOLO Detection Results:
{detections}

Generate a Solar Panel Inspection Report.

1. Problem Description
- Explain what defect was detected.
- Mention the confidence score.
- Explain it in simple English.

2. Damage Level

Provide the following information:

• Severity: (Low / Medium / High)

• Performance Impact:
Explain how the detected defect affects the solar panel's power generation.

• Risk:
Explain what may happen if the defect is not repaired.

• Inspection Note:
If the exact crack depth or internal damage cannot be determined from a single image, clearly mention it.

Write 1-2 short sentences.

3. Recommended Solution

Provide the following information:

• Immediate Action:
Explain what should be done first.

• Maintenance:
Explain how to prevent the issue from becoming worse.

• Replacement:
Mention whether repair or replacement is recommended.

• Future Prevention:
Give one recommendation to avoid similar defects.

Write 1-2 short sentences.

4. Possible Cause

• Explain the most likely causes.
• Examples:
- Thermal stress
- Manufacturing defect
- Dust accumulation
- Aging
- Loose electrical connection
- Mechanical impact

Use simple English.


Do NOT write long paragraphs.




"""


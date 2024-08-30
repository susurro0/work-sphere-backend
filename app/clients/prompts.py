from datetime import datetime


def create_report_prompt(example_text: str, cues: str) -> str:
    prompt = f"""
    You are a safety inspector tasked with creating a new safety report. 

    **Example Report:**
    {example_text}

    **New Cues:**
    {cues}

    Using the example report as a guide, generate a new safety report that reflects the style and structure of the example. Incorporate all relevant details from the new cues into the report.
    """

    return prompt.strip()

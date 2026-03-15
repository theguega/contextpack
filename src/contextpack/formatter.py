from .models import ContextPackResult

def format_context_pack(result: ContextPackResult) -> str:
    """
    Formats the context pack result as markdown for LLM consumption.
    """
    lines = [
        "# ContextPack Results",
        "",
        f"Question: {result.query}",
        "",
        "Sources:"
    ]
    
    unique_domains = sorted(list(set(s.domain for s in result.sources if s.domain)))
    for domain in unique_domains:
        lines.append(f"- {domain}")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for chunk in result.chunks:
        lines.append(chunk.text)
        lines.append("")
        lines.append("---")
        lines.append("")
        
    return "\n".join(lines)

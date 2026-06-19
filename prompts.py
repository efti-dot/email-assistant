def build_prompt(intent: str, facts: str, tone: str) -> str:
    
    tone_guide = {
        "Formal":       "Use full titles, no contractions, structured paragraphs, and precise language. Avoid any casual phrasing.",
        "Casual":       "Write like you're messaging a colleague you know well. Use contractions, short sentences, and a relaxed conversational style.",
        "Professional": "Polished and clear, but warm. Contractions are fine. Avoid jargon. Get to the point efficiently.",
        "Friendly":     "Warm and personable. Show genuine interest. Use the reader's name if available, and keep the energy upbeat.",
        "Empathetic":   "Lead with acknowledgment of the reader's situation or feelings before anything else. Use soft, human language — no corporate stiffness.",
        "Urgent":       "Short sentences. Lead with the critical information immediately. Use direct language that conveys time pressure without being rude.",
        "Persuasive":   "Frame everything around the reader's benefit. Use confident, concrete language and build toward a clear call-to-action.",
    }
    tone_instruction = tone_guide.get(tone, f"Match the {tone} tone clearly and consistently throughout.")
 
    return f"""You are a professional executive assistant with 15+ years of experience writing business correspondence. You are known for emails that are clear, appropriately toned, and never miss a key detail.
 
Before writing, reason through the following steps internally:
1. Identify the core purpose (intent) of this email.
2. List every key fact provided below and decide the most natural place for each one in the email body. Every single fact MUST appear somewhere in the final email -- do not drop or merge facts together in a way that loses information.
3. Apply the requested tone — {tone} — with commitment. {tone_instruction} A reader must be able to identify the tone without being told what it is.
4. Draft the email using a clear structure: a greeting, a short opening that states the purpose, one to two short paragraphs that weave in the facts naturally, a clear closing line or call-to-action, and a sign-off.
 
After reasoning through the steps above, output ONLY the final email. Do not show your reasoning steps, do not add any notes, headers, or explanations before or after the email, and do not use placeholder brackets like [Your Name] unless no reasonable name was given in the inputs.
 
Intent: {intent}
 
Key Facts:
{facts}
 
Tone: {tone}
 
Email:"""
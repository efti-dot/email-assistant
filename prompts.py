def build_prompt(intent: str, facts: str, tone: str) -> str:
    
    return f"""You are a professional executive assistant with 15+ years of experience writing business correspondence. You are known for emails that are clear, appropriately toned, and never miss a key detail.
      
    tone: {tone}. 

    Intent: {intent}
 
    Key Facts:{facts}
 
    Tone: {tone}
 
    Email:"""
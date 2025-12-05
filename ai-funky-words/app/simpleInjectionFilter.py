"""
Original code sourced from: 
    OWASP "LLM Prompt Injection Prevention" - Primary Defense, Input Validation & Defense
    https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html

Modified slightly for challenge purposes (to be vulnerable to typoglycemia attacks).
"""


class PromptInjectionFilter:
    def __init__(self):
        self.dangerous_patterns = [
            r'(new|ignore|disregard|forget|bypass|override)\s*(\S+\s*)*(the|your|any|all)?\s*(\S+\s*)*(previous|prior|former|past|old)?\s*(instructions?|orders?)\s*',
            r'(clear|reset)\s*(\S+\s*)*(the\s*)?(\S+\s*)*(context|conversation|chat)',
            r'you\s*(\S+\s*)*are\s*(\S+\s*)*now\s*(\S+\s*)*.+',
            r'(disable|bypass|ignore)\s*(\S+\s*)*(safety|filters?|restrictions?)',
            r'(what|explain|talk|tell|reveal|show|dump|print)\s*(\S+\s*)*(system|hidden|internal)\s*(\S+\s*)*(prompt|instructions?)',
            r'system\s*(\S+\s*)*override',
            r'(what|give|reveal|pass|send|return|dump|print)\s*(\S+\s*)*(the|your)?\s*(\S+\s*)*(flag?)'
        ]

    def detect_injection(self, text: str) -> bool:
        # First, normalize the text (removes mixed symbols/numbers in the middle of words)
        text = self.normalize(text)

        for pattern in self.dangerous_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return True
        return False


    def normalize(self, text: str) -> str:
        # Tokenize the input by splitting on whitespace
        tokens = text.split(" ")
        
        # Process each token
        normalized_tokens = []
        for token in tokens:
            if token == " ":
                continue
            # If the token has a mix of letters + numbers/symbols in the middle, delete it
            if re.search(r'[a-zA-Z]+[0-9!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]+[a-zA-Z]+', token):
                continue  # Skip invalid token
            normalized_tokens.append(token)  # Keep valid token

        # Join the valid tokens back into a single string with spaces
        normalized_text = ' '.join(normalized_tokens)
        return normalized_text.strip()  # Remove any extra leading/trailing spaces


    def sanitize_input(self, text: str) -> str:
        # First, normalize the text (removes mixed symbols/numbers in the middle of words)
        text = self.normalize(text)
        
        # Now, sanitize the input with regex filtering (similar to your previous method)
        for pattern in self.dangerous_patterns:
            text = re.sub(pattern, '[FILTERED]', text, flags=re.IGNORECASE)
        
        return text[:10000]  # Limit length


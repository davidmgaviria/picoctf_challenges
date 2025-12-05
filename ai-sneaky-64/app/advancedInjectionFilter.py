
import re
from difflib import get_close_matches


class PromptInjectionFilter:
    
    def __init__(self):
        self.dangerous_patterns = [
            r'(new|ignore|disregard|forget|bypass|override)\s*(\S+\s*)*(the|your|any|all)?\s*(\S+\s*)*(previous|prior|former|past|old)?\s*(instructions?|orders?|internal)\s*',
            r'(clear|reset)\s*(\S+\s*)*(the\s*)?(\S+\s*)*(context|conversation|chat)',
            r'you\s*(\S+\s*)*are\s*(\S+\s*)*now\s*(\S+\s*)*.+',
            r'(disable|bypass|ignore)\s*(\S+\s*)*(safety|filters?|restrictions?)',
            r'(what|explain|talk|tell|reveal|show|dump|print)\s*(\S+\s*)*(system|hidden|internal)\s*(\S+\s*)*(prompt|instructions?)',
            r'system\s*(\S+\s*)*override',
            r'(what|give|reveal|pass|send|return|dump|print)\s*(\S+\s*)*(the|your)?\s*(\S+\s*)*(flag?)'
        ]
        # Flatten all keywords in patterns for normalization
        self.keywords = [
            "new","ignore","disregard","forget","bypass","override",
            "the","your","any","all","previous","prior","former","past","old",
            "instructions","orders","clear","reset","context","conversation","chat",
            "are","now","disable","safety","filters","restrictions","what","explain",
            "talk","tell","reveal","show","dump","print","system","hidden","internal",
            "override","give","pass","send","return","flag"
        ]


    def detect_injection(self, text: str) -> bool:
        normalized_text = self.normalize_keywords(text)
        #print("Normalized text: %s" % normalized_text)
        for pattern in self.dangerous_patterns:
            if re.search(pattern, normalized_text, re.IGNORECASE):
                return True
        return False


    def normalize_keywords(self, text: str) -> str:
        tokens = text.split()
        normalized_tokens = []

        for token in tokens:
            # Correct typos or leet variants
            match = get_close_matches(token.lower(), self.keywords, n=1, cutoff=0.6)  # make it pretty sensitive so even very misspelled words will be detected 
            if match:
                normalized_tokens.append(match[0])
            else:
                normalized_tokens.append(token)
        return ' '.join(normalized_tokens)


    def sanitize_input(self, text: str) -> str:
        normalized_text = self.normalize_keywords(text)
        for pattern in self.dangerous_patterns:
            normalized_text = re.sub(pattern, '[FILTERED]', normalized_text, flags=re.IGNORECASE)
        return normalized_text[:10000]


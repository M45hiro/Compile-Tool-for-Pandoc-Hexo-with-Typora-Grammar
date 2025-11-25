import os
import re

class Compiler:
    def __init__(self, path):
        """
        :str path: path of markdowns to be compiled
        """
        self.path = path

    @property
    def md_file_paths(self):
        return [
            os.path.join(root, file)
            for root, _, files in os.walk(self.path)
            for file in files
            if file.lower().endswith(".md")
        ]

    def rectify(self, content):
        """Remove spaces around $ unless inside backticks"""
        return re.sub(r'(?<!`)\$ | \$ (?!`)', '$', content)

    def readMarkdown(self, md_file_path):
        with open(md_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return self.rectify(content)

    def getSingleEquations(self, markdown_content):
        """Return list of inline equations"""
        cleaned = re.sub(r'`.*?`', '', markdown_content, flags=re.DOTALL)
        return re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', cleaned, flags=re.DOTALL)

    def innerExpressionCompile(self, expression, backslash_replacement="\\\\\\"):
        """Compile inline math expression"""
        regexEscape = r"(\\boldsymbol\{[^\}]+\}|\\[a-zA-Z]+)"
        escape_iter = list(re.finditer(regexEscape, expression))
        escape_spans = [(m.start(), m.end(), m.group()) for m in escape_iter]

        regexSub = r"_[a-zA-Z]+"
        sub_spans = []
        for m in re.finditer(regexSub, expression):
            s, e = m.start(), m.end()
            if not any(es <= s < ee for es, ee, _ in escape_spans):
                sub_spans.append((s, e, m.group()))

        regexOther = r"[^\\\sA-Za-z_]"
        other_spans = []
        for m in re.finditer(regexOther, expression):
            s, e = m.start(), m.end()
            if not any(es <= s < ee for es, ee, _ in escape_spans) and \
               not any(ss <= s < se for ss, se, _ in sub_spans):
                other_spans.append((s, e, m.group()))

        regexLetters = r"[a-zA-Z]+"
        taken = set()
        for s, e, _ in escape_spans + other_spans:
            taken.update(range(s, e))
        letters_spans = []
        for m in re.finditer(regexLetters, expression):
            s, e = m.start(), m.end()
            if all(i not in taken for i in range(s, e)):
                letters_spans.append((s, e, m.group()))
                taken.update(range(s, e))

        all_spans = []
        for s, e, t in escape_spans:
            all_spans.append((s, e, 'escape', t))
        for s, e, t in sub_spans:
            all_spans.append((s, e, 'sub', t))
        for s, e, t in other_spans:
            all_spans.append((s, e, 'other', t))
        for s, e, t in letters_spans:
            all_spans.append((s, e, 'letters', t))
        all_spans.sort(key=lambda x: x[0])

        out_parts = []
        idx = 0
        span_idx = 0
        n = len(expression)
        while idx < n:
            if span_idx < len(all_spans) and all_spans[span_idx][0] == idx:
                s, e, typ, text = all_spans[span_idx]
                if typ == 'escape':
                    out_parts.append(text.replace("\\", backslash_replacement))
                elif typ == 'sub' or typ == 'other':
                    out_parts.append(text)
                else:
                    out_parts.append("\\\\\\textit{" + text + "}")
                idx = e
                span_idx += 1
            else:
                out_parts.append(expression[idx])
                idx += 1

        return "".join(out_parts)

    def compile(self):
        md_paths = self.md_file_paths
        output_dir = os.path.join(os.path.dirname(self.path), "output")
        os.makedirs(output_dir, exist_ok=True)

        for md_path in md_paths:
            content = self.readMarkdown(md_path)

            
            # Inline equations
            inline_eqs = self.getSingleEquations(content)
            for eq in inline_eqs:
                compiled = self.innerExpressionCompile(eq)
                content = content.replace(f"${eq}$", f"${compiled}$")
            
            content = content.replace(r'\label', r'\\\label')
            content = content.replace(r'\quad', r'\\\quad')
            content = content.replace(r'\notag', r'\\\notag')
            
            
            # Write output
            out_path = os.path.join(output_dir, os.path.basename(md_path))
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)

        return output_dir


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    compiler = Compiler("source")
    out_dir = compiler.compile()
    print("Compiled markdown output to:", out_dir)
# compiler_logic.py
import re

class Compiler:
    def __init__(self):
        pass

    def rectify(self, content):
        """Remove spaces around $ unless inside backticks"""
        return re.sub(r'(?<!`)\$ | \$ (?!`)', '$', content)

    def getSingleEquations(self, markdown_content):
        """Return list of inline equations"""
        # 注意：这里简单的 replace 可能会有副作用，但在不改变你原逻辑的前提下保留
        cleaned = re.sub(r'`.*?`', '', markdown_content, flags=re.DOTALL)
        return re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', cleaned, flags=re.DOTALL)

    def innerExpressionCompile(self, expression, backslash_replacement="\\\\\\"):
        """Compile inline math expression (你的原始逻辑)"""
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

    def compile_content(self, content):
        """直接处理字符串内容，不涉及文件IO"""
        # 1. Rectify
        content = self.rectify(content)

        # 2. Get Inline Equations
        inline_eqs = self.getSingleEquations(content)
        
        # 3. Compile Equations and Replace
        # 使用 set 去重避免重复处理，按长度降序排列防止包含关系的替换错误
        unique_eqs = sorted(list(set(inline_eqs)), key=len, reverse=True)
        
        for eq in unique_eqs:
            # 如果原始公式中有特殊正则字符，需要转义后再进行替换查找
            compiled = self.innerExpressionCompile(eq)
            # 简单的 replace 可能会误伤，但在当前架构下维持原样
            # 注意：这里需要转义 eq 才能在 replace 中安全使用，或者直接用 string replace
            content = content.replace(f"${eq}$", f"${compiled}$")
        
        # 4. Global Replacements
        content = content.replace(r'\label', r'\\\label')
        content = content.replace(r'\quad', r'\\\quad')
        content = content.replace(r'\notag', r'\\\notag')
        
        return content
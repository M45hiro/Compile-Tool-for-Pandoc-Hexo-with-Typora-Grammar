import streamlit as st
from compiler_logic import Compiler

st.set_page_config(page_title="Markdown Math Compiler", page_icon="📝")

st.title("📝 Markdown 公式编译器")
st.write("上传你的 `.md` 文件，我们将自动处理其中的行内公式格式。")

# 实例化编译器
compiler = Compiler()

# 文件上传组件
uploaded_file = st.file_uploader("选择一个 Markdown 文件", type=["md"])

if uploaded_file is not None:
    # 读取文件内容
    string_data = uploaded_file.getvalue().decode("utf-8")
    
    st.info("文件上传成功，正在处理...")
    
    try:
        # 调用核心逻辑
        processed_content = compiler.compile_content(string_data)
        
        st.success("编译完成！")
        
        # 显示部分预览
        with st.expander("查看处理后的内容预览"):
            st.text(processed_content[:1000] + "\n..." if len(processed_content) > 1000 else processed_content)

        # 下载按钮
        st.download_button(
            label="下载编译后的 .md 文件",
            data=processed_content,
            file_name=f"compiled_{uploaded_file.name}",
            mime="text/markdown"
        )
        
    except Exception as e:
        st.error(f"处理过程中发生错误: {e}")
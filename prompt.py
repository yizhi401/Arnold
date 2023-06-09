"""
0. 存储被测代码到向量数据库，以langchain为例，开发单元测试 -- DONE
1. 提交source code，基于llm提取相关方法(后续可以考虑优化这一步不用llm)
2. 从向量数据库查询相关context
3. 组装context和source code，提交给gpt生成代码

"""

GENTEST_PREFIX_TEMPL = """
你需要为一些代码生成测试用例。在生成用例的过程中，你有两种选择:

1. 一种是直接生成，如果你认为已经有足够多的信息来生成测试用例
2. 询问代码的功能，如果你认为还需要查看代码更多的上下文信息

你可以自由询问代码的功能，我会告诉你与这段代码相关的内容和代码片段，重复这个过程，直到你认为已经收集到了足够多的信息，然后开始生成测试用例。

------------------------------------------------------------------------------------
待生成测试用例的代码如下：

{target_code}

------------------------------------------------------------------------------------

如果你希望了解上述代码片段的细节，你可以按照下列格式继续询问：

请给我关于```code```更多的信息，包括它的定义和使用方式。

你可以将```code```替换为你希望了解的代码片段。

如果你认为已经收集到了足够多的信息，请接下来为目标代码生成测试用例，并用Markdown格式返回测试用例代码。

"""

GENTEST_PROCESS_TEMPL2 = """
human： 关于```{code}```的相关信息如下：
{context}


"""

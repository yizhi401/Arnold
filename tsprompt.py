"""Testcase Prompt"""


GENRAL_INSTRUCTION = """Generate testcases based on the given code block below. You may find the "Code Description" and "Related Codes" to help you generate testcases, but you only need to generate testcases for the codes in "Code Under Tets" section.
If no suitable test cases can be generated, simply responses with "Cannot generate valid test cases". Your response should use {{ language }} programming language and {{ test_libraries }} libraries. You should genearte testcases step by step with
complete code comments. Your testcases should consider all possible conditions. Please return code wrapped inside markdown delimiter, don't make extra explanation. This code should be able to directly write into source file and run after compilation.

Code Description:

{{ desc }}

Related Codes:

{{ related_codes }}

Code Under Test:

{{ code }}

TestCases:"""

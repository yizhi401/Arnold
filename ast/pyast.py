import os
import pathlib
from pycparser import c_parser, c_ast, parse_file


class FunctionVisitor(c_ast.NodeVisitor):
    """
    用来遍历抽象语法树的访问器类
    """

    def __init__(self, target_name):
        self.target_name = target_name
        self.found = False
        self.source = ""

    def visit_FuncDef(self, node):
        if node.decl.name == self.target_name:
            self.found = True
            self.source = node.__class__(node.coord).show()

    def visit_Decl(self, node):
        if node.name == self.target_name:
            self.found = True
            self.source = node.__class__(node.coord).show()


def find_code_for_target(target_name, project_path):
    """
    在C语言工程项目中查找目标函数/变量的代码

    Args:
        target_name (str): 目标函数/变量的名称
        project_path (str): C语言工程项目的根目录路径

    Returns:
        str: 包含目标函数/变量的源代码字符串，如果找不到则返回空字符串
    """

    parser = c_parser.CParser()
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".c"):
                file_path = os.path.join(root, file)
                try:
                    ast = parse_file(file_path, use_cpp=True)
                except c_parser.ParseError:
                    # 跳过无法解析的源代码文件
                    continue

                visitor = FunctionVisitor(target_name)
                visitor.visit(ast)

                if visitor.found:
                    return visitor.source

    return ""


def main():
    project_path = pathlib.Path(__file__).parent.parent.parent / 'algorithms'
    target_name = "keylog"
    source_code = find_code_for_target(target_name, project_path)
    if source_code:
        print(source_code)
    else:
        print("Not found")


if __name__ == "__main__":
    main()

import ast
import networkx as nx

class StaticAnalyzer:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)
        self.control_flow_graph = nx.DiGraph()
        self.data_flow_graph = nx.DiGraph()
        self.critical_data = set()

    def build_control_flow_graph(self):
        
        prev_block = None  

        for node in ast.walk(self.tree):
            block_id = id(node)
            self.control_flow_graph.add_node(block_id, ast_node=node)

            if prev_block:
                
                self.control_flow_graph.add_edge(prev_block, block_id)
            prev_block = block_id

            if isinstance(node, ast.If):

                for body_node in node.body:
                    if isinstance(body_node, (ast.Assign, ast.Expr, ast.If)):
                      self.control_flow_graph.add_edge(block_id, id(body_node))

                for orelse_node in node.orelse:
                    if isinstance(orelse_node, (ast.Assign, ast.Expr, ast.If)):
                        self.control_flow_graph.add_edge(block_id, id(orelse_node))




        print("Control Flow Graph Edges:")
        for source, target in self.control_flow_graph.edges:
            print(f"  {source} -> {target}")


    def build_data_flow_graph(self):
        class DFGVisitor(ast.NodeVisitor):
            def __init__(self, dfg):
                self.dfg = dfg
                self.current_scope = {}  

            def visit_Assign(self, node):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_var = target.id
                        used_vars = []
                        for used_node in ast.walk(node.value):
                            if isinstance(used_node, ast.Name):
                                used_vars.append(used_node.id)
                        for used_var in used_vars:
                            self.dfg.add_edge(used_var, defined_var)

                        
                        if isinstance(node.value, ast.Call):
                                for arg in node.value.args:
                                    for n in ast.walk(arg):
                                        if isinstance(n, ast.Name):
                                            self.dfg.add_edge(n.id, defined_var)
                        self.current_scope[defined_var] = True

            def visit_If(self, node):

                for child_node in node.body:
                    self.visit(child_node)
                for child_node in node.orelse:
                    self.visit(child_node)

                for test_node in ast.walk(node.test):
                    if isinstance(test_node, ast.Name):
                        test_var = test_node.id
                        if test_var in self.current_scope:
                            for body_node in node.body:
                                if isinstance(body_node, ast.Expr) and isinstance(body_node.value, ast.Call):
                                    self.dfg.add_edge(test_var, body_node.value.func.id)
                                elif isinstance(body_node, ast.Assign):
                                    for target in body_node.targets:
                                        if isinstance(target, ast.Name):
                                            self.dfg.add_edge(test_var, target.id)
        visitor = DFGVisitor(self.data_flow_graph)
        visitor.visit(self.tree)

        print("Data Flow Graph Edges:")
        for source, target in self.data_flow_graph.edges:
              print(f"  {source} -> {target}")


    def identify_critical_data(self):
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name) and (node.id.startswith("user_input") or node.id.startswith("config")):
                self.critical_data.add(node.id)
        if self.critical_data:
            print("Critical Data Identified:")
            for var in self.critical_data:
                print(f"  - {var}")
        else:
            print("No Critical Data Identified.")


    def analyze(self):
        self.build_control_flow_graph()
        self.build_data_flow_graph()
        self.identify_critical_data()
        return self.control_flow_graph, self.data_flow_graph, self.critical_data
class Instrumentation:
    def __init__(self, control_flow_graph, data_flow_graph, critical_data):
        self.cfg = control_flow_graph
        self.dfg = data_flow_graph
        self.critical_data = critical_data

    def inject_instrumentation(self, code):
        instrumented_code = []
        for line in code.split('\n'):
   
            if any(var in line for var in self.critical_data):
                instrumented_code.append(f"  # START CHECKDEF for critical data")
                instrumented_code.append(f"  CHECKDEF({line})")
                instrumented_code.append(f"  # END CHECKDEF for critical data")
            instrumented_code.append(line)
        return '\n'.join(instrumented_code)

    def optimize_instrumentation(self, code):
        
        optimized_code = []
        for line in code.split('\n'):
            if "CHECKDEF" in line and "non_critical_var" in line:
                continue  
            optimized_code.append(line)
        return '\n'.join(optimized_code)
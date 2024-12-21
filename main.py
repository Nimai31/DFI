from static_analysis import StaticAnalyzer
from instrumentation import Instrumentation
from runtime_enforcement import RuntimeEnforcer
from textwrap import dedent  

if __name__ == "__main__":
   
    input_code = dedent("""
    config_auth = 0
    packet = read_packet()
    if authenticate(packet):
        config_auth = 1
    if config_auth:
        process_packet(packet)
    """)




    
    analyzer = StaticAnalyzer(input_code)
    cfg, dfg, critical_data = analyzer.analyze()

    
    instrumenter = Instrumentation(cfg, dfg, critical_data)
    instrumented_code = instrumenter.inject_instrumentation(input_code)
    print("\nInstrumented Code:\n", instrumented_code)

    
    enforcer = RuntimeEnforcer()
    operations = [
        {'type': 'SETDEF', 'address': 'config_auth', 'identifier': 1},
        {'type': 'CHECKDEF', 'address': 'config_auth', 'expected_set': {1}}
    ]
    enforcer.enforce(operations)
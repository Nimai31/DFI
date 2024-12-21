class RuntimeEnforcer:
    def __init__(self):
        self.rdt = {}  

    def set_def(self, address, identifier):
        self.rdt[address] = identifier
        print(f"SETDEF: {address} -> {identifier}")

    def check_def(self, address, expected_set):
        if address in self.rdt and self.rdt[address] in expected_set:
            print(f"CHECKDEF Passed: {address}")
            return True
        print(f"CHECKDEF Failed: {address}")
        return False

    def enforce(self, operations):
        for op in operations:
            if op['type'] == 'SETDEF':
                self.set_def(op['address'], op['identifier'])
            elif op['type'] == 'CHECKDEF':
                self.check_def(op['address'], op['expected_set'])

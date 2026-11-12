import camp.main
import inspect

print("camp.main file:", camp.main.__file__)
print("--- camp.main source ---")
print(inspect.getsource(camp.main))
print("--- dir(camp.main) ---")
print([name for name in dir(camp.main) if "bp" in name or "main" in name or "Blueprint" in name])
import sys
from .generators import generate_readme, update_structure

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "readme"
    
    if command == "readme":
        generate_readme()
    elif command == "structure":
        update_structure()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

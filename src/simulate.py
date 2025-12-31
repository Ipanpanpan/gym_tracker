from models import ExerciseMetadata, ExerciseSet, Unit
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run_simulation():
    console.print(Panel.fit("Gym Tracker Logic Simulation", style="bold magenta"))

    # 1. Define Exercises
    bench_press = ExerciseMetadata(name="Bench Press", is_assisted=False)
    assisted_pullup = ExerciseMetadata(name="Assisted Pull-up", is_assisted=True)

    # 2. Simulate Bench Press (Standard)
    # Set A: 200 Lbs
    # Set B: 85 Kg (~187 Lbs) -> 200 Lbs should be better
    
    bp_set_a = ExerciseSet(bench_press, 200, Unit.LBS, 5)
    bp_set_b = ExerciseSet(bench_press, 85, Unit.KG, 5)

    verify_comparison(bp_set_a, bp_set_b)

    # 3. Simulate Assisted Pull-up (Inverse)
    # Set C: 20 Kg Assist
    # Set D: 10 Kg Assist (Harder/Better)
    
    ap_set_c = ExerciseSet(assisted_pullup, 20, Unit.KG, 8)
    ap_set_d = ExerciseSet(assisted_pullup, 10, Unit.KG, 8)

    verify_comparison(ap_set_d, ap_set_c) # Expect D > C

    # 4. Mixed Unit Assisted
    # Set E: 40 Lbs (~18 Kg)
    # Set F: 15 Kg (Better than 18 Kg/40 Lbs)
    
    ap_set_e = ExerciseSet(assisted_pullup, 40, Unit.LBS, 5)
    ap_set_f = ExerciseSet(assisted_pullup, 15, Unit.KG, 5)
    
    verify_comparison(ap_set_f, ap_set_e)

def verify_comparison(set1, set2):
    table = Table(title=f"Comparing {set1.exercise.name}")
    table.add_column("Set 1", style="cyan")
    table.add_column("Set 2", style="green")
    table.add_column("Better?", style="bold yellow")
    table.add_column("Reason", style="white")

    is_better = set1.is_better_than(set2)
    
    reason = ""
    s1_kg = set1.normalized_kg
    s2_kg = set2.normalized_kg
    
    if set1.exercise.is_assisted:
        reason = f"{s1_kg:.2f}kg VS {s2_kg:.2f}kg (Lower is Better)"
    else:
        reason = f"{s1_kg:.2f}kg VS {s2_kg:.2f}kg (Higher is Better)"

    table.add_row(
        str(set1),
        str(set2),
        "Set 1" if is_better else "Set 2 (or equal)",
        reason
    )
    
    console.print(table)
    
    # Plain text fallback for debug
    print(f"\n[VERIFY] Comparing {set1.exercise.name}:")
    print(f"  {set1} VS {set2}")
    print(f"  Result: {'Set 1 is Better' if is_better else 'Set 2 is Better'}")
    print(f"  Reason: {reason}")


if __name__ == "__main__":
    run_simulation()

from models import ExerciseMetadata, ExerciseSet, Unit

def run():
    print("START VERIFICATION")
    
    # Bench Press
    bench = ExerciseMetadata(name="Bench Press", is_assisted=False)
    bp1 = ExerciseSet(bench, 200, Unit.LBS, 5) # ~90.7kg
    bp2 = ExerciseSet(bench, 85, Unit.KG, 5)   # 85kg
    
    print(f"Bench: {bp1.normalized_kg:.2f}kg vs {bp2.normalized_kg:.2f}kg")
    if bp1.is_better_than(bp2):
        print("PASS: 200lbs > 85kg")
    else:
        print("FAIL: 200lbs should be better")

    # Assisted Pullup
    pullup = ExerciseMetadata(name="Assisted Pull-up", is_assisted=True)
    ap1 = ExerciseSet(pullup, 10, Unit.KG, 8)
    ap2 = ExerciseSet(pullup, 20, Unit.KG, 8)
    
    print(f"Pullup: {ap1.weight}kg vs {ap2.weight}kg")
    if ap1.is_better_than(ap2):
        print("PASS: 10kg assist > 20kg assist")
    else:
        print("FAIL: 10kg assist should be better")

    # Mixed Assisted
    ap3 = ExerciseSet(pullup, 15, Unit.KG, 5)
    ap4 = ExerciseSet(pullup, 40, Unit.LBS, 5) # ~18.1kg
    
    print(f"Mixed: {ap3.normalized_kg:.2f}kg vs {ap4.normalized_kg:.2f}kg")
    if ap3.is_better_than(ap4):
        print("PASS: 15kg > 40lbs (18kg)")
    else:
        print("FAIL: 15kg should be better")

if __name__ == "__main__":
    run()

import flet as ft
from database import Database
from models import Unit, ExerciseSet

db = Database()

def main(page: ft.Page):
    page.title = "Gym Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # Navigation handling
    def route_change(route):
        page.views.clear()
        
        # Home View
        view = ft.View(
            "/",
            [
                ft.AppBar(title=ft.Text("Gym Tracker"), bgcolor=ft.colors.SURFACE_VARIANT),
                create_home_view(page)
            ],
        )
        page.views.append(view)

        # Detail View
        if page.route.startswith("/exercise/"):
            try:
                ex_id = int(page.route.split("/")[-1])
                page.views.append(
                    ft.View(
                        f"/exercise/{ex_id}",
                        [
                            ft.AppBar(title=ft.Text("Exercise Details"), bgcolor=ft.colors.SURFACE_VARIANT),
                            create_detail_view(page, ex_id)
                        ]
                    )
                )
            except ValueError:
                pass
                
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.push_route(page.route)



def create_home_view(page):
    exercises = db.get_exercises()
    
    lv = ft.ListView(expand=True, spacing=10)
    
    for ex in exercises:
        # ex: (id, name, is_assisted, desc)
        ex_id, name, is_assisted, _ = ex
        icon = ft.icons.FITNESS_CENTER
        if is_assisted:
            icon = ft.icons.ACCESSIBILITY_NEW
            
        lv.controls.append(
            ft.Card(
                content=ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(icon),
                        title=ft.Text(name),
                        subtitle=ft.Text("Assisted" if is_assisted else "Standard"),
                        on_click=lambda e, eid=ex_id: page.go(f"/exercise/{eid}")
                    ),
                    padding=10
                )
            )
        )
    
    return lv

def create_detail_view(page, exercise_id):
    exercise_meta = db.get_exercise_by_id(exercise_id)
    history = db.get_history(exercise_id)
    
    # Inputs
    weight_tf = ft.TextField(label="Weight", keyboard_type=ft.KeyboardType.NUMBER, width=100)
    reps_tf = ft.TextField(label="Reps", keyboard_type=ft.KeyboardType.NUMBER, width=100)
    unit_dd = ft.Dropdown(
        width=80,
        options=[ft.dropdown.Option("kg"), ft.dropdown.Option("lbs")],
        value="kg"
    )

    def add_set_click(e):
        if not weight_tf.value or not reps_tf.value:
            return
            
        try:
            w = float(weight_tf.value)
            r = int(reps_tf.value)
            u = Unit(unit_dd.value)
            
            db.add_set(exercise_id, w, u, r)
            
            # Refresh
            page.go(f"/exercise/{exercise_id}") # Hacky refresh
            page.update()
            
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid Input"))
            page.snack_bar.open = True
            page.update()

    # History List
    history_lv = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, expand=True)

    # Calculate Best Set for Display Highlighting
    best_set_idx = -1
    if history:
        # Convert all to ExerciseSet objects for comparison
        sets_objs = []
        for i, h in enumerate(history):
            # h: id, weight, unit, reps, timestamp
            s = ExerciseSet(
                exercise=exercise_meta,
                weight=h[1],
                unit=Unit(h[2]),
                reps=h[3]
            )
            sets_objs.append((i, s))
        
        # Sort using is_better_than
        if sets_objs:
            # Sort desc (best first)
            # bubble sort or just max
            best_idx = 0
            for i in range(1, len(sets_objs)):
                if sets_objs[i][1].is_better_than(sets_objs[best_idx][1]):
                    best_idx = i
            
            best_set_idx = sets_objs[best_idx][0]


    for i, h in enumerate(history):
        # h: id, weight, unit, reps, timestamp
        weight_display = f"{h[1]} {h[2]}"
        is_best = (i == best_set_idx)
        
        history_lv.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(f"{h[1]} {h[2]} x {h[3]}", size=16, weight=ft.FontWeight.BOLD if is_best else ft.FontWeight.NORMAL),
                    ft.Text(h[4], size=12, color=ft.colors.GREY),
                    ft.Icon(ft.icons.STAR, color=ft.colors.YELLOW) if is_best else ft.Container()
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10,
                bgcolor=ft.colors.SURFACE_VARIANT if is_best else None,
                border_radius=5
            )
        )

    return ft.Column([
        ft.Text(exercise_meta.name, size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Logic: " + ("Lower is Better (Assisted)" if exercise_meta.is_assisted else "Higher is Better"), color=ft.colors.GREY),
        
        ft.Divider(),
        
        ft.Row([
            weight_tf,
            unit_dd,
            reps_tf,
            ft.IconButton(ft.icons.ADD, on_click=add_set_click, bgcolor=ft.colors.PRIMARY, icon_color=ft.colors.ON_PRIMARY)
        ]),
        
        ft.Divider(),
        ft.Text("History", size=18, weight=ft.FontWeight.BOLD),
        history_lv
    ], expand=True)

if __name__ == "__main__":
    ft.app(target=main)

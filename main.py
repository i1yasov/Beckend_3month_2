import flet as ft
from db import main_db

def main_page(page:ft.Page):
    page.title = 'ToDo List'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column()

    def view_task(task_id, task_text):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)
        
        def delete_edit(_):
            main_db.delete_task(task_id=task_id)
            new_list = []
            for item in task_list.controls:
                if item.task_id != task_id:
                    new_list.append(item)
            task_list.controls = new_list
            page.update()
        
        delete_button = ft.IconButton(icon=ft.Icons.DELETE,icon_color=ft.Colors.RED,
        on_click=delete_edit
)

        def save_edit(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            page.update()
        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_edit)
        
        def enable_edite(_):
            if task_field.read_only == True:
                task_field.read_only = False
            else:
                task_field.read_only = True
            page.update()
        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edite)
        
        row = ft.Row([task_field, edit_button,save_button,delete_button])
        row.task_id = task_id
        return row
    
    def add_task_flet(_):
        if task_input.value:
            task_text = task_input.value.strip()
            task_id = main_db.add_task(task=task_text)
            task_input.value = None
            task_list.controls.append(view_task(task_id= task_id,task_text=task_text) )
            page.update()
    task_input = ft.TextField(label='Введите задачу',on_submit=add_task_flet)
    
    page.add(task_input,task_list)

if __name__ =='__main__':
    main_db.init_db()
    ft.app(main_page)

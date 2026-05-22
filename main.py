import flet as ft
from db import main_db

def main_page(page:ft.Page):
    page.title = 'ToDo List'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=20,scroll = ft.ScrollMode.AUTO,expand=True)

    filter_type = 'all'

    def load_tasks(filter_type):
            task_list.controls.clear()
            for task_id , task, completed in main_db.get_task(filter_type):
                task_list.controls.append(view_task(task_id=task_id,
                task_text=task,completed = completed))
            page.update()

    def delete_completed(_):
        main_db.delete_completed()
        load_tasks(filter_type)
    delete_completed_button =ft.ElevatedButton('Очистить выполненные',on_click=delete_completed)
    
    def view_task(task_id, task_text, completed = None):

        task_field = ft.TextField(value=task_text, expand=True, read_only=True,)

        check_box = ft.Checkbox(value=bool(completed),
        on_change=lambda e : toggle_task(task_id=task_id,
        is_completed=e.control.value))
        
        def delete_edit(_):
            main_db.delete_task(task_id=task_id)
            load_tasks(filter_type)
        
        delete_button = ft.IconButton(icon=ft.Icons.DELETE,icon_color=ft.Colors.RED,
        on_click=delete_edit)

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
        
        row = ft.Row([check_box,task_field, edit_button,save_button,delete_button])
        row.task_id = task_id
        return row
    
    def toggle_task(task_id,is_completed):
        print(is_completed)
        main_db.update_task(task_id=task_id, completed= int(is_completed))
        print(int(is_completed))
        load_tasks(filter_type)

    def add_task_flet(_):
        if task_input.value:
            task_text = task_input.value.strip()
            task_id = main_db.add_task(task=task_text)
            task_input.value = None
            task_list.controls.append(view_task(task_id= task_id,task_text=task_text) )
            page.update()

    
    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks(filter_type)
    task_input = ft.TextField(label='Введите задачу',on_submit=add_task_flet)

    filter_button = ft.Row([
        ft.ElevatedButton('Все задачи',on_click=lambda e:set_filter('all')),
        ft.ElevatedButton('В работе',on_click=lambda e: set_filter('uncompleted')),
        ft.ElevatedButton('Готово',on_click=lambda e: set_filter('completed'))
    ],alignment = ft.MainAxisAlignment.SPACE_AROUND )

    page.add(task_input,delete_completed_button,filter_button,task_list)
    load_tasks(filter_type)


if __name__ =='__main__':
    main_db.init_db()
    ft.app(main_page)
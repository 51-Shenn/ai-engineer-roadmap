import os
import uuid as uid

def view_all_task(tasks=[]):
    print('\nTo-do list:')
    if not tasks:
        print('- Empty\n')
        return
    for i, t in enumerate(tasks):
        print(f'{i+1}. {t}')
    print()

# add task
def add_task(tasks=[]):
    new_task = input('Enter your task: ')
    tasks.append(new_task)

    print('Task added.')
    print()
    view_all_task(tasks)

    return tasks

# remove task:
def remove_task(tasks=[]):
    view_all_task(tasks)

    task_num = input('Which task would you want to remove?: ')
    task_num = int(task_num)

    if task_num <= 0 or task_num > len(tasks):
        print('Invalid task number. Please try again.\n')
        return tasks

    tasks.pop(task_num - 1)

    print('Task removed.')
    print()
    view_all_task(tasks)

    return tasks

def update_task(tasks=[]):
    view_all_task(tasks)

    task_num = input('Which task would you want to update?: ')
    task_num = int(task_num)

    if task_num <= 0 or task_num > len(tasks):
         print('Invalid task number. Please try again.\n')
         return tasks

    task_update = input('Update your task to?: ')

    tasks[int(task_num) - 1] = task_update

    print('Task updated.')
    print()
    view_all_task(tasks)

    return tasks

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    tasks = []
    print("\n=== CLI TO-DO LIST ===\n")
    print("Your Current Tasks: ")

    if not tasks:
        print('- Empty')
    else:
        view_all_task(tasks)

    print()
    print('1. Add new task')
    print('2. Update task')
    print('3. Remove task')
    print('4. View all tasks')
    print('0. Exit')

    print()
    choice = -1

    while choice != 0:
        choice = input('Enter choice: ')

        match int(choice):
            case 1:
                tasks = add_task(tasks)
            case 2:
                tasks = update_task(tasks)
            case 3:
                tasks = remove_task(tasks)
            case 4:
                view_all_task(tasks)
            case 0:
                return
            case _:
                print('Please try again.')

if __name__ == "__main__":
    main()

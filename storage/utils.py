from django.core.files.storage import get_storage_class

base = 'task-management/project-{}-task-{}/'
storage = get_storage_class()()


def get_basepath(project_pk, task_pk):
    return base.format(project_pk, task_pk)


def get_files(project_pk, task_pk):
    current_path = get_basepath(project_pk, task_pk)
    file_names = [item for item in storage.listdir(current_path)[1]]
    return [{'filename': item, 'size': storage.size(current_path + item)} for item in file_names]


def get_file(project_pk, task_pk, filename):
    current_path = get_basepath(project_pk, task_pk)
    return storage.open(current_path + filename)


def delete_file(project_pk, task_pk, filename):
    current_path = get_basepath(project_pk, task_pk)
    return storage.delete(current_path + filename)

def exists_file(project_pk, task_pk, filename):
    current_path = get_basepath(project_pk, task_pk)
    return storage.exists(current_path + filename)


def save_file(project_pk, task_pk, filename, file):
    current_path = get_basepath(project_pk, task_pk)
    return storage.save(current_path + filename, file)

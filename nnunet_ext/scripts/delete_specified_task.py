import os
import argparse
from nnunet_ext.paths import nnUNet_raw_data
from batchgenerators.utilities.file_and_folder_operations import join
from nnunet_ext.utilities.helpful_functions import delete_dir_con, delete_task

def main(use_parser=True, **kwargs):
    r"""This function can be used to delete a specified task, ie. all preprocessed, planned and cropped data
        generated by the nnUNet or the extension.
        This function can also be used after a failed test to be sure that the generated data is deleted competely.
    """
    # -- Use the ArgumentParser if desired -- #
    if use_parser:
        # -----------------------
        # Build argument parser
        # -----------------------
        # -- Create argument parser and add one argument -- #
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--task_ids", nargs="+", help="Specify a list of task ids for which the data should be removed. Each of these "
                                                                "ids must have a matching folder 'TaskXXX_' in the raw "
                                                                "data folder")
        parser.add_argument('--test_data', action='store_true', default=False,
                            help='Specify if the test data should be removed automatically. This needs to be done when '
                                ' the pytest \'test_all_trainers\' failed and the generated data still exists after the test.'
                                ' Default: False')
        
        # -- Extract parser arguments -- #
        args = parser.parse_args()
        test = args.test_data
        tasks = args.task_ids    # List of the tasks
    # -- When internally using the function, we do not want an ArgumentParser, so provide positional arguments properly -- #
    else:
        # -- Extract arguments from positional arguments -- #
        test = kwargs['test_data']      # Boolean if include test data
        tasks = kwargs['task_ids']      # List of the tasks IDs
    
    # -- If the tasks are None, then set them as an empty list so the loop will not fail -- #
    if tasks is None:
        tasks = list()

    # -- When no task is provided and we do not remove test_data, print a Note -- #
    if len(tasks) == 0 and not test:
        print('Note: No tasks are provided, so no tasks are removed, be aware of that.')
    
    # -- Remove test data as well if desired -- #
    if test:
        # -- Extract all existing tasks as long as there is a dash '-' in the name -- #
        # -- Our generated tasks have a '-' in the name so we can differentiate between them -- #
        test_tasks = [x for x in os.listdir(nnUNet_raw_data) if 'Task-' in x] # Only those we generated, do not delete other data!
        # -- Add those test_task ids to tasks to be removed -- #
        for test_t in test_tasks:
            # -- Extract the task id and add it to the tasks list for deletion -- #
            tasks.append(test_t.split('_')[0][-3:])
        
        # -- Extract the base path the same way as in the pytest --> if it is not the same there will be a mixup. -- #
        folder_to_delete = join(os.path.dirname(os.path.realpath(nnUNet_raw_data)), "tmp_for_testing")
        # -- Delete the directory if it exists -- #
        if os.path.isdir(folder_to_delete):
            delete_dir_con(folder_to_delete)
    
    # -- Loop through tasks and remove them, test data is included if it was desired -- #
    for task_id in tasks:
        # -- Make 3 digit task id out of it -- #
        task_id = "%03.0d" % int(task_id)
        
        # -- Delete the specified task data folders that have been created by the nnUNet (-extension). -- #
        delete_task(task_id)


if __name__ == '__main__':
    main()
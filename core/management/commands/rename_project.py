import glob
import os
import re
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Rename the Project"

    def add_arguments(self, parser):
        # get current project name and new project name as an arguments
        parser.add_argument(
            "old_project_name", nargs="+", type=str, help="current project name"
        )
        parser.add_argument(
            "new_project_name",
            nargs="+",
            type=str,
            help="new_project_name project name",
        )

    def handle(self, *args, **options):
        old_project_name = options["old_project_name"][0]
        new_project_name = options["new_project_name"][0]

        # make a list of files, needs to be renamed
        base = str(settings.BASE_DIR)
        projectfiles = []
        projectfiles.extend(
            [
                os.path.join(base, "manage.py"),
                os.path.join(base, "common/tasks.py"),
                os.path.join(base, ".pre-commit-config.yaml"),
            ]
        )
        projectfiles += glob.glob(os.path.join(base, old_project_name, "*.py"))
        projectfiles += glob.glob(os.path.join(base, old_project_name, "**", "*.py"))

        data_dict = {
            f"{old_project_name}.": f"{new_project_name}.",
            f'"{old_project_name}"': f'"{new_project_name}"',
            f"'{old_project_name}'": f'"{new_project_name}"',
            f"{old_project_name}/": f"{new_project_name}/",
        }
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, data_dict.keys())))

        # replace the code content with new project name
        for pythonfile in projectfiles:
            with open(pythonfile, "r") as file:
                filedata = file.read()

            # For each match, look-up corresponding value in dictionary
            filedata = regex.sub(
                lambda mo: data_dict[mo.string[mo.start() : mo.end()]], filedata
            )

            with open(pythonfile, "w") as file:
                file.write(filedata)

        # rename the directory
        try:
            shutil.move(old_project_name, new_project_name)
        except Exception:
            pass

        self.stdout.write(
            self.style.SUCCESS("Project has been renamed to %s" % new_project_name)
        )

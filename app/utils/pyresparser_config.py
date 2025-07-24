import os
import pkg_resources
from pathlib import Path


def create_pyresparser_config():
    """Create the missing config.cfg file for pyresparser"""
    try:
        # Get the pyresparser package location
        pyresparser_path = pkg_resources.get_distribution('pyresparser').location
        config_dir = os.path.join(pyresparser_path, 'pyresparser')
        config_file = os.path.join(config_dir, 'config.cfg')

        # Create config directory if it doesn't exist
        os.makedirs(config_dir, exist_ok=True)

        # Default configuration content
        config_content = '''[DEFAULT]
# PyResParser Configuration File

[SKILLS]
skills_file = skills.csv

[EDUCATION]
education_file = education.csv

[EXPERIENCE]
experience_file = experience.csv
'''

        # Write the config file
        with open(config_file, 'w') as f:
            f.write(config_content)

        print(f"Created config file at: {config_file}")
        return True

    except Exception as e:
        print(f"Failed to create config file: {e}")
        return False
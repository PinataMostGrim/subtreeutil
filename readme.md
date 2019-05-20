# subtreeutil

Automates checking out files and folders from a remote repository.

## Features

- Adds a remote repository to an existing local one
- Checks out a list of files and folders from a branch
- (Optionally) Moves files and folders to a new location
- (Optionally) Cleans up (deletes) files or folders
- Removes the temporary remote

## Usage
- **Create or edit a configuration file**
    Use the `subtree config` command and supply a configuration filename to edit
- **Perform an automated checkout operation**
    Use the `subtree checkout` command and supply a configuratione filename to consume
- **View usage options**
    Use the `subtree -h` command

## Configuration Settings
A template configuration file can be viewed at `config\template.json` or use the `subtree config` command to generate a default configuration.

- **remote_name**
    - The name to give the remote we are adding
    - *Default:* ***"subtree"***
- **remote_url**
    - The URL of the remote to add
    - *Default:* ***""***
- **branch**
    - The branch to checkout sources from
    - *Default:* ***"develop"***
- **source_paths**
    - A list of files or folders to checkout from the remote repository
    - *Default:* ***"[]"***
- **destination_paths**
    - A list of locations to move the checked out sources into. If any `destination_paths` are defined at all, the number of entries must match the number of entries in `source_paths`.
    - *Default:* ***"[]"***
- **cleanup_paths**
    - A list of files or folders to delete after the checkout and move steps have been performed.
    - *Default:* ***"[]"***

## Examples
##### Edit a configuration file
```
subtree config config\template.json
```

##### Perform an automated checkout using a configuration file
```
subtree checkout config\template.json
```

##### Example configuration file
```json
{
    "remote_name": "framework",
    "remote_url": "git@github.com:User/Framework.git",
    "branch": "develop",
    "source_paths": ["Assets\\Framework\\", "Assets\\Framework.meta"],
    "destination_paths": ["UnitySDK\\Assets\\Framework", "UnitySDK\\Assets\\Framework.meta"],
    "cleanup_paths": ["Assets"]
}
```

## Notes
- A local repository must be present in the current working directory.
- Subtree uses relative paths. It is best to execute the CLI script from the local repository's root folder.
- Configuration files are formatted using json
- A log file is created at `logs\subtree_cli.log`

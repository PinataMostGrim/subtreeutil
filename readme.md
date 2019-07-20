# subtreeutil
Automates checking out files and folders from a remote git repository where a submodule or subtree is not convenient to use.

Performs a checkout operation from a remote repository with the following steps:
- Adds a remote to an existing local repository
- Checks out a list of files and folders from a branch
- (Optionally) Moves files and folders to a new location
- (Optionally) Cleans up (deletes) files or folders
- Removes the temporary remote

## Usage
```
usage: subtree_cli [-h] {checkout,config} ...

Application that automates checking out files and folders from a remote git
repository.

optional arguments:
  -h, --help         show this help message and exit

Commands:
  {checkout,config}
    checkout         Perform a checkout operation using the specified
                     configuration file
    config           Create or edit a checkout operation configuration file
```

## Configuration Settings
A template configuration file can be viewed at `config\template.json` or use the `subtreeutil config` command to generate a default configuration.

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
subtreeutil config config\template.json
```

##### Perform an automated checkout using a configuration file
```
subtreeutil checkout config\template.json
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
- A repository must be present in the current working directory
- `subtreeutil` uses relative paths. It is best to execute the CLI script from the local repository's root folder.
- A log file is created at `logs\subtree_cli.log`
- `subtreeutil` does not remove files that were deleted on the remote repository but are still present on the local one

# Paralenz video recombiner

The paralenz is a good camera but annoyingly cuts the videos into chunks at it saves them which you either need to use their crappy software to recombine or do it by hand. Or you can point this at the directory that contains the videos and it will figure out which videos belong together and recombine them for you.

## Usage

```
pl_recombine.exe <path_to_directory>
```

path_to_directory is normally just the path to the 100PRLNZ directory containing the videos.

## Installing

In the `dist` folder there is a prebuilt single exe for windows that you can run standalone. To run the python, first sync the repo and then run (on Windows, Unix's you will need to do by hand)

```
setup_env.bat
.pyenv\Scripts\activate
python pl_recombine.py <path_to_directory>
```

## Building the standalone exe

Setup the python virtual environment as above then run to generate the exe in the `dist` folder.

```
pyinstaller pl_recombine.spec
```

# shrinkpdf
Inspired by this 
[gist](https://gist.github.com/firstdoit/6390547). 

Use this script to resize/reduce/shrink large pdfs. Feel free to share.

# Installation
### Requires: 
- python3. Install from 
[python.org](https://www.python.org/downloads/)
- ghostscript

### Mac OS & Linux
- On Mac, install ghostscript using: ```brew install ghostscript```. On Linux, use ```sudo apt install ghostscript``` (tested on Ubuntu 18.04)
- Clone this repo or download [shrink.py](https://github.com/DanAbara/shrinkpdf/blob/main/shrink.py) to your PC.
- Run ```sudo chmod +x shrink.py``` from terminal to make the file executable. 
- Test install. Run ```./shrink.py -h``` to view help.

### Windows
- Install ghostscript from https://www.ghostscript.com/
- Clone the repo or download [shrink.py](https://github.com/DanAbara/shrinkpdf/blob/main/shrink.py) to your PC.
- Use ```python shrink.py -h``` to test install.

# Usage
    $ ./shrink.py [-h] [-i IN_FILE] [-v VERBOSE] [-q QUALITY]

    optional arguments:
    -h, --help            show this help message and exit
    -i, --in_file         Path to input PDF file. Eg. input.pdf
    -q, --quality         Compression quality: screen, ebook, printer, prepress, default. 
    -v, --verbose         Output updates while program is running, default True.

The compression level goes from **screen** as the strongest yielding smaller output files, to **default** as the weakest yielding higher output files.

### Example

    $ ./shrink.py -i test.pdf
    File checks done...
    Shrinking file test.pdf...
    Compression quality: default...
    Done. PDF reduced by 38.18%, Output size: 7.01 MB.
    Resized file written to: /home/daniel/Documents/shrinkpdf/test_resized.pdf.


On Windows, use:
    
    > python shrink.py -i test.pdf
    

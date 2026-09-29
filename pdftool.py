#!/usr/bin/python3

"""
Author: D. Abara

Shrinks the size of a PDF. There are five levels of compression:
        - default: weakest level -> larger output files
        - prepress
        - printer
        - ebook
        - screen: strongest level -> smaller output files

Unlocks a PDF so that future access does not require a password. 
The unlock password is required. 

Both shrink and unlock can be done but must be done separately.

"""

from sys import platform
import os.path
import subprocess
import argparse

def _validate_file(in_file):
    """
    Checks that the input file exists and the file type is 'pdf'. 
    :param in_file: The path to file to be checked
    :return: bool
    """
    if not os.path.isfile(in_file):
        print(f"Error: invalid path for input file {in_file}. File not found")
        return False
     
    if in_file.split('.')[-1].lower() != 'pdf':
        print(f"Error: input file must have .pdf extension.")
        return False

    return True
  


def _get_platform():
    """
    Check the os platform to determine the right ghostscript command to run
    """
    if platform == 'win32':
        return 'gswin64'

    return 'gs'



def shrink_pdf(in_file, quality, verbose):
    """
    :param in_file: The path to file whose size is to be shrinked.
    :param quality: Level of compression.
    :param verbose: Show output as program runs
    :return: None
    """

    if ( _validate_file(in_file) ):
        if verbose:
            print("File checks done...")

        # check os
        cmd = _get_platform()

        # begin file reduction
        start_size = round(float(os.path.getsize(in_file)/1e6), 2)
        if verbose:
            print(f"Shrinking file {in_file}...")
            print(f"Compression quality: {quality}...")
        
        out_file = in_file.split('.')[0]+'_resized.pdf'
        subprocess.run([cmd, 
                        '-sDEVICE=pdfwrite', 
                        '-dCompatibilityLevel=1.4',
                        '-dPDFSETTINGS=/{}'.format(quality), 
                        '-dNOPAUSE', 
                        '-dQUIET', 
                        '-dBATCH',
                        '-sOutputFile={}'.format(out_file), 
                        in_file]
                   )
        output_size = round(float(os.path.getsize(out_file)/1e6), 2)
        reduction = round(((start_size - output_size) / start_size) * 100, 2)
        if verbose:
            print('Done. PDF reduced by {}%, Output size: {} MB.'.format(reduction, output_size))
            print('Resized file written to: {}.'.format(os.path.realpath(out_file)))



def unlock_pdf(in_file, pword, verbose):
    """
    :param in_file: The path to file whose password is to be removed
    :return: None
   
    """
    if ( _validate_file(in_file) ):
        if verbose:
            print("File checks done...")

        cmd = _get_platform()

        # begin decrypting of pdf file
        if verbose:
            print(f"Decrypting pdf file {in_file}...")

        out_file = in_file.split('.')[0]+'_unlocked.pdf'
        subprocess.run([cmd, 
                        '-sDEVICE=pdfwrite',
                        '-dCompatibilityLevel=1.7',
                        '-dNOPAUSE',
                        '-dQUIET',
                        '-dBATCH',
                        '-dEmbedAllFonts=true',
                        '-sPDFPassword={}'.format(pword),
                        '-sOutputFile={}'.format(out_file),
                        in_file]
                       )
        if verbose:
            print("Done. PDF password removed.")
            print(f"Unlocked File written to: {os.path.realpath(out_file)}")



def main():
    parser = argparse.ArgumentParser(description="Two functions:\n"
                                        "1. Shrinks the size of a PDF file and writes the reduced file to the current directory,\n"
                                        "2. Unlocks a PDF given the password,\n"
                                        "param in_file: Mandatory - The path to file whose size is to be shrinked,\n" 
                                        "param pword: Mandatory - The password of the PDF file to be unlocked,\n"  
                                        "param quality: Level of compression default lowest; optional for size reduction,\n" 
                                        "param verbose: Show output as program runs default True.")

    parser.add_argument('-f', '--func', dest='func', type=str, 
                        help='Desired function, set either "shrink" or "unlock", Required', required=True)
    parser.add_argument('-i', '--in_file', dest='in_file',
                        type=str, help='Path to input PDF file. Eg. input.pdf, Required', required=True)
    parser.add_argument('-p', '--pword', dest='pword',
                        type=str, help='Password of PDF file, Only required if --func is set to "unlock"')
    parser.add_argument('-q', '--quality', dest='quality', type=str, default='default',
                        help='Compression quality: screen, ebook, printer, prepress, default.')
    parser.add_argument('-v', '--verbose', dest='verbose', type=bool, default=True,
                        help='Output updates while program is running, default True.')
    
    args = parser.parse_args()

    if ( args.func == 'shrink' ):
        shrink_pdf(args.in_file, args.quality, args.verbose)

    if ( args.func == 'unlock' ):
        if not args.pword:
            parser.error("--pword is required when --func is set to 'unlock'.")

        unlock_pdf(args.in_file, args.pword, args.verbose)

if __name__=='__main__':
    main()

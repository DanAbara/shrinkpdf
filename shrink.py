#!/usr/bin/python3

"""
Author: D. Abara
Date: 08/07/2021

Shrinks the size of a PDF. There are five levels of compression:
        - default: weakest level -> larger output files
        - prepress
        - printer
        - ebook
        - screen: strongest level -> smaller output files
"""

from sys import platform
import os.path
import subprocess
import argparse


def shrink_pdf(in_file, quality, verbose):
    """
    :param in_file: The path to file whose size is to be shrinked.
    :param out_file: The path to output file produced by the program.
    :param quality: Level of compression.
    :param verbose: Show output as program runs
    :return: None
    """
    if not os.path.isfile(in_file):
        print('Error: invalid path for input file {}. File not found.'.format(in_file))
    elif in_file.split('.')[-1].lower() != 'pdf':
        print('Error: input file must have .pdf extension.')
    else:
        if verbose:
            print("File checks done...")
        # check os
        if platform == 'win32':
            cmd = 'gswin64'
        else:
            cmd = 'gs'
        # begin file reduction
        start_size = round(float(os.path.getsize(in_file)/1e6), 2)
        if verbose:
            print(f'Shrinking file {in_file}...')
            print(f'Compression quality: {quality}...')
        
        out_file = in_file.split('.')[0]+'_resized.pdf'
        subprocess.run([cmd, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS=/{}'.format(quality), '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    '-sOutputFile={}'.format(out_file), in_file]
                   )
        output_size = round(float(os.path.getsize(out_file)/1e6), 2)
        reduction = round(((start_size - output_size) / start_size) * 100, 2)
        if verbose:
            print('Done. PDF reduced by {}%, Output size: {} MB.'.format(reduction, output_size))
            print('Resized file written to: {}.'.format(os.path.realpath(out_file)))


def main():
    parser = argparse.ArgumentParser(description="Shrink the size of a PDF and writes the reduced file to the current directory," 
                                        "\n:param in_file: Mandatory - The path to file whose size is to be shrinked," 
                                        "\n:param quality: Level of compression default lowest," 
                                        "\n:param verbose: Show output as program runs default True.")
    parser.add_argument('-i', '--in_file', dest='in_file',
                        type=str, help='Path to input PDF file. Eg. input.pdf', required=True)
    parser.add_argument('-q', '--quality', dest='quality', type=str, default='default',
                        help='Compression quality: screen, ebook, printer, prepress, default.')
    parser.add_argument('-v', '--verbose', dest='verbose', type=bool, default=True,
                        help='Output updates while program is running, default True.')
    
    args = parser.parse_args()
    shrink_pdf(args.in_file, args.quality, args.verbose)


if __name__=='__main__':
    main()

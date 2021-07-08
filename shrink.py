#!/usr/bin/python3

""" Author: D. Abara

"""

import sys
from sys import platform
import os.path
import subprocess
import argparse


def check_pdf(in_file):
    # check file exists and is pdf
    if os.path.isfile(in_file) and in_file.split('.')[-1].lower() == 'pdf':
        return True
    else:
        return False


def shrink_pdf(in_file, out_file, quality='default', verbose=True):
    """
    Shrinks the size of a PDF. There are five levels of compression
        - default: weakest level of compression -> larger output files
        - prepress
        - printer
        - ebook
        - screen: strongest level of compression -> smaller output files

    :param in_file: The path to file whose size is to be shrinked.
    :param out_file: The path to output file produced by the program.
    :param quality: Level of compression.
    :param verbose: Show output as program runs
    :return: None
    """
    if not check_pdf(in_file):
        print('Error: Check that file exists and that it is has .pdf extension.')
    else:
        if verbose:
            print("File checks done.")
        # check os
        if platform == 'win32':
            cmd = 'gswin64'
        else:
            cmd = 'gs'
        # begin file reduction
        start_size = round(float(os.path.getsize(in_file)/1e6), 2)
        if verbose:
            print('Shrinking Pdf...'.format(start_size))
        subprocess.run([cmd, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS=/{}'.format(quality), '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    '-sOutputFile={}'.format(out_file), in_file]
                   )
        output_size = round(float(os.path.getsize(out_file)/1e6), 2)
        reduction = round(((start_size - output_size) / start_size ) * 100, 2)
        if verbose:
            print('PDF reduced by {}% \nOutput size: {} MB '.format(reduction, output_size))
            print('Done.')


def main():
    parser = argparse.ArgumentParser(description='Shrink the size of a PDF.')
    parser.add_argument('-i', '--in_file', dest='in_file',
                        type=str, help='Path to input PDF file whose size is to be reduced')
    parser.add_argument('-o', '--out_file', dest='out_file', type=str,
                        help='Path to compressed PDF file')
    parser.add_argument('-v', '--verbose', dest='verbose', type=bool,
                        help='Output updates while program is running, default True.')
    parser.add_argument('-q', '--quality', dest='quality', type=str,
                        help='Compression quality: screen, ebook, printer, prepress, default. '
                             '\nStrongest compression level is "screen" -> Smaller output file size.'
                             '\nWeakest compression level is "default" -> Larger output file size.')

    args = parser.parse_args()
    shrink_pdf(args.in_file, args.out_file)


if __name__=='__main__':
    main()

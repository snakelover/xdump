import os
from optparse import OptionParser

def xdump(filename, blocksize, decimal, encoding):
    """Opens given file and reads blocks of blocksize length."""

    fh = open(filename, "rb")
    count = 0
    base = "X" if not decimal else "d"
    end = fh.seek(0, os.SEEK_END)
    fh.seek(0)
    number = blocksize // 4 if blocksize % 4 != 0 else (blocksize // 4) - 1
    size = number + blocksize * 2
    print("{0: <8}\t{1: <{size}}\t{encoding} characters".format("Block", "Bytes",
                                size=size, encoding=encoding, blocksize=blocksize))
    print("{0:-^8}\t{1:-^{size}}\t{2:-<{blocksize}}".format("", "", "",
                                        size=size, blocksize=blocksize))
    while True:
        block = fh.read(blocksize)
        i = 0
        hex_bytes =""
        for byte in block:
            i += 1
            hex_bytes += "{0:02X}".format(byte)
            if i % 4 == 0 and i != blocksize:
                hex_bytes += " "
        decoded_string = ""
        for char in block.decode(encoding, 'replace'):
            if char.isprintable() and char != '\ufffd':
                decoded_string  += char
            else:
                decoded_string  += "."
        print("{0:0>8{base}}\t{1: <{size}}\t{2: <{blocksize}}".format(count, hex_bytes,
                decoded_string , base=base, size=size, blocksize=blocksize))
        if fh.tell() == end:
            break
        count += 1
        
def main():

    parser = OptionParser(usage="Usage: %prog [options] [file1 [file2 [... fileN]]]")
    parser.add_option("-b", "--blocksize", action="store", type="int", default=16,
                      dest="blocksize", help="block size (8..80) [default: %default]")
    parser.add_option("-d", "--decimal", action="store_true", default=False,
                      dest="decimal", help="decimal block numbers [default: hexadecimal]")
    parser.add_option("-e", "--encoding", action="store", type="string", default="UTF-8",
                      dest="encoding", help="encoding (ASCII..UTF-32) [default: %default]")

    (opts, args) = parser.parse_args()

    if len(args) < 1:
        print("error")
    if not (8 <= opts.blocksize <= 80):
        print("error")

    for filename in args:
        xdump(filename, opts.blocksize, opts.decimal, opts.encoding)

main()

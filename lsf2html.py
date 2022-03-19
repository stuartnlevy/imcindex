#! /usr/bin/env python3

import sys, os
import csv
import time

class GoogleURL(object):


    @staticmethod
    def url(fid, fmime):
        pfx = GoogleURL.prefix_for(fmime)
        return pfx + fid

    p_folder = "https://drive.google.com/drive/u/0/folders/" 
    p_document = "https://docs.google.com/document/d/"
    p_file = "https://docs.google.com/file/d/"

    file_mime0 = set(['text', 'image', 'audio', 'video', 'application'])
    file_specialcase = set(['application/pdf', 'application/postscript', 'application/rtf'])

    @staticmethod
    def prefix_for(fmime):
        if fmime == "inode/directory":
            return GoogleURL.p_folder

        if fmime.startswith('application/vnd.google-apps'):
            return GoogleURL.p_document

        # other things, including other application/ things, are probably plain files
        mime0 = fmime.split('/')[0]
        if mime0 in GoogleURL.file_mime0:
            return GoogleURL.p_file
        if fmime in GoogleURL.file_specialcase:
            return GoogleURL.p_file

        #raise ValueError("What type for " + fmime + "?")
        print("What type for %s?" % fmime, file=sys.stderr)
        return GoogleURL.p_file


unique = False
outstemfmt = "imcindex.%Y-%m-%d"
drivename = "imcdrive"
lsffile = None
doit = (len(sys.argv) > 1)


ii = 1
while ii < len(sys.argv) and sys.argv[ii][0] == '-':
    opt = sys.argv[ii]; ii += 1
    if opt == '-u':
        unique = True
    elif opt == '-o':
        outstemfmt = sys.argv[ii]; ii += 1
    elif opt == '-lsf':
        lsffile = sys.argv[ii]; ii += 1
    elif opt == '-drive':
        drivename = sys.argv[ii]; ii += 1
    elif opt == '-doit':
        pass
    else:
        if opt not in ('-h', '--help'):
            print("Unknown option: ",opt)
        doit = False
        break

if not doit:
    print(f"""Usage: 
   rclone lsf --format istmp --recursive --separator '	' imcdrive: > imcfiles.lsf-istmp  # with a <Tab> for the argument to --separator
   {sys.argv[0]} [options]
Scans a Google Drive file tree using rclone lsf, writes .csv and .html files listing its contents.  Options:

   -drive <drivename>   (-drive {drivename})  Scan that named 'remote drive', as set up with 'rclone config'
   -o  <outstem>        (-o {outstemfmt})  Basename of output file.  %'s are processed by strftime(3), so %Y-%m-%d includes the date.
   -lsf somefile  Use cached results from rclone lsf --format istmp --separator '<Tab>' > somefile.  Otherwise runs rclone internally.
   -doit                Do the default thing, including running rclone.

With no options at all, just prints this Usage message.   So, to do the default thing, without changing above settings:

   {sys.argv[0]} -doit

Writes HTML to <outstem>.html, and a CSV table to <outstem>.csv.
If we run rclone internally, its output is saved in <outstem>.lsf-istmp """, file=sys.stderr)
    sys.exit(1)


if lsffile is None:
    snapshotdate = time.localtime()
    outbase = time.strftime( outstemfmt, snapshotdate ) # timestamp is current moment
    rclone_lsf_file = f"{outbase}.lsf-istmp"

    cmd = f"rclone lsf --format istmp --recursive --separator '\t' {drivename}: > '{rclone_lsf_file}'"
    print(f"Running rclone: {cmd}")
    rslt = os.system(cmd)

    if rslt != 0:
        print("Trouble using rclone to scan the remote drive '{drivename}'.")
        print("For advice on setting up rclone, see README.md.")
        sys.exit(1)

else:
    rclone_lsf_file = lsffile # file as produced by 'rclone lsf --format istmp --separator "	" imcdrive:'
    snapshotdate = time.localtime( os.path.getmtime( rclone_lsf_file ) )  # time tuple 
    outbase = time.strftime( outstemfmt, snapshotdate )

with open(rclone_lsf_file, 'r') as inf:
    ents = []
    for line in inf.readlines():
        ss = line.rstrip().split('\t')
        if len(ss) == 5:
            ents.append(ss)

if unique:
    ents.sort( key = lambda ss: ss[3] )
else:
    ents.sort( key = lambda ss: ss[4] )

already = set()
prevdir = None

timestampstr = time.strftime( '%Y-%m-%d %H:%M', snapshotdate )

print(f"Writing {outbase}.html and {outbase}.csv")

with open(outbase + '.html', 'w') as htmlf:
    print("<H1>IMC Google Drive documents as of %s</H1>" % timestampstr, file=htmlf)
    print("<TABLE BORDER=1>", file=htmlf)
    print("<TR><TD>Size(bytes)<TD>Last Modified<TD>Path", file=htmlf)

    for ss in ents:
        fid, fsize, fdate, fmime, fname = ss

        if unique:
            if fmime in already:
                continue
            already.add(fmime)

        fdir = os.path.dirname(fname)
        if fdir != prevdir:
            if prevdir is not None:
                print("<TR><TD>&nbsp;<TD><TD>", file=htmlf)
            prevdir = fdir
        ##isdir = (fmime == "inode/directory")
        ##if isdir:
        ##    fsize = "-"
        if fsize == "-1":
            fsize = ""
        url = GoogleURL.url(fid, fmime)
        fdate = fdate.replace(' ', '&nbsp;')
        
        if unique:
            print("<TR><TD>%s<TD>%s<TD>%s<TD><a href=\"%s\">%s</a>" % (fsize, fdate, fmime, url, fname), file=htmlf)
        else:
            print("<TR><TD>%s<TD>%s<TD><a href=\"%s\">%s</a>" % (fsize, fdate, url, fname), file=htmlf)
    print("</TABLE>", file=htmlf)

csvfields = [ 'id', 'size', 'time', 'mimetype', 'path', 'url' ]
with open(outbase+'.csv', 'w') as csvstream:
    csvw = csv.DictWriter( csvstream, csvfields )
    csvw.writeheader()
    for ss in ents:
        fid, fsize, fdate, fmime, fname = ss
        csvw.writerow( { 'id':fid, 'size':fsize, 'time':fdate, 'mimetype':fmime,  'path':fname, 'url':GoogleURL.url(fid, fmime) } )

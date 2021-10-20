```
$ vcardtool --help
Usage: vcardtool [OPTIONS] COMMAND [ARGS]...

Options:
  --verbose
  --debug
  --help     Show this message and exit.

Commands:
  split

$ vcardtool split --help
Usage: vcardtool split [OPTIONS] VCF_FILE OUTPUT_DIR

Options:
  --verbose
  --debug
  --help     Show this message and exit.

$ cat contacts.vcf
BEGIN:VCARD
VERSION:3.0
N:;john;;;
FN:john
TEL;TYPE=cell:321-654-0987
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:;mike;;;
FN:mike
TEL;TYPE=cell:+1-123-456-7890
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:;kara;;;
FN:kara
TEL;TYPE=cell:456-789-0123
END:VCARD

$ mkdir _extracted

$ vcardtool split contacts.vcf _extracted/

$ ls _extracted/
total 12K
   0 drwxr-xr-x 2 user user 100 2021-10-20 16:10:22 .
   0 drwxrwxrwx 7 root root 440 2021-10-20 16:10:07 ..
4.0K -rw-r--r-- 1 user user 148 2021-10-20 16:10:22 contacts.vcf__1.vcf
4.0K -rw-r--r-- 1 user user 151 2021-10-20 16:10:22 contacts.vcf__2.vcf
4.0K -rw-r--r-- 1 user user 148 2021-10-20 16:10:22 contacts.vcf__3.vcf

$ cat _extracted/contacts.vcf__3.vcf
BEGIN:VCARD
VERSION:3.0
UID:8af86db2fe4f585f56b05506cd0573651b677ff88e255c5aee55bfe82b13ca96
N:;kara;;;
FN:kara
TEL;TYPE=cell:456-789-0123
END:VCARD
```

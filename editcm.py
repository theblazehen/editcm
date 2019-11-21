#!/usr/bin/python3

import subprkubectless, yaml, sys, tempfile

cm_name = sys.argv[1]

cm_in_yaml = subprkubectless.check_output(['kubectl', 'get', 'cm', '-o', 'yaml', cm_name])

cm = yaml.load(cm_in_yaml)

tmpdir = tempfile.mkdtemp()

for file in cm['data']:
    disk_file = f"{tmpdir}/{file}"
    outfile = open(disk_file, 'w')
    outfile.write(cm['data'][file])
    outfile.close()
    subprkubectless.run(['sensible-editor', disk_file])
    cm['data'][file] = open(disk_file).read()

cm_outfile = open(f"{tmpdir}/cm.yaml", 'w')
yaml.dump(cm, cm_outfile)
cm_outfile.close()

subprkubectless.run(['kubectl', 'replace', '-f', f"{tmpdir}/cm.yaml"])
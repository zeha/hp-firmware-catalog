#!/usr/bin/python

try:
	import json
except:
	import simplejson as json

import sys,os,subprocess
from datetime import datetime

# fw contains the firmware and further informations
# structure
# Key: ['OurLinkedName', flag]
# types:
# - 0 don't download automatically - key not uniq!
# - 1 autoupdate - keys are uniq and can be used
# - 2 Disk - handled special

fwdir = './firmware'

fws={
       # G6
       'P64': {'ourname': 'DL360G6_BIOS.scexe', 'type': 1},
       'PowerPIC-Electra': {'ourname': 'DL3xxGx_POWERMGMT.scexe', 'type': 0},
       'PIC24K20': {'ourname': 'DL360G6_BACKPLANE.scexe', 'type': 1},
       # G5
       'P58': {'ourname': 'DL360G5_BIOS.scexe','type': 1},
       'PowerPIC-Iris-DL360G5': {'ourname': 'DL360G5_POWERMGMT.scexe', 'type':1},
       # SA E200i
       '3212103C':{'ourname': 'SA_E200_FW.scexe', 'type': 1},
       # SA P400(i)
       '3234103C':{'ourname': 'SA_P400_FW.scexe', 'type': 1},
       # SA P410i
       '3241103C':{'ourname': 'SA_P410_FW.scexe', 'type': 1},
       # IloV2
       'RI7':{'ourname': 'ILO2_FW.scexe', 'type': 1},
       # Disks
       # DG072BABCE, and DF146BABCF drives
       'DG072BABCE':{'type': 2},
       # DG0072BALVL, DG0146BALVN, DG0146BAHZP, DG0300BALVP, and DG0300BAHZQ drives
       'DG0072BALVL':{'type':2},
       # DG0300FAMWN, DG0146FAMWL
       'DG0300FAMWN':{'type':2},
       # DG072ABAB3, DG072BB975, DG146ABAB4, and DG146BB976 drives
       'DG072ABAB3':{'type':2},
       # DG0300FARVV, DG0146FARVU drives
       'DG0300FARVV': {'type': 2},
       # DG072A4951, DG072BAAJA, DG146BAAJB, and DG146A4960
       # not found in catalog - current file - CP010008.scexe
       # DG072A4951, DG072BAAJA, DG146BAAJB, and DG146A4960 drives
       # not found in catalog - current file - CP010008.scexe
       #['','-']
      }

def ensure_directory(path):
        if not os.path.exists(path): os.mkdir(path)
def updateinventory(f,i):
  ver = fws[i]['version']
  f.write("filename: %s\n" % (ver['filename']))
  f.write("key %s, type %s\n" % (i,0 if not fws[i].has_key('type') else fws[i]['type']))
  f.write("name: %s\n" % (ver['name']))
  f.write("version : %s\n" % (ver['version']))
  f.write("url: %s\n" % (ver['url']))
  f.write("ourname: %s\n" % (fws[i]['ourname'] if fws[i].has_key('ourname') else ""))
  f.write("=========================================================================================================")

def download(filename, url):
  curl_opts = ["curl","-o",filename]
  curl_opts.append(url)
  if subprocess.call(curl_opts) != 0:
    return 1
  os.chmod(filename, 0755)
  return 0

ensure_directory(fwdir)

# generate list
f = file('catalog.json')
x = json.load(f)
for i in fws:
  for j in x['entries']:
    if j.has_key('sw_keys') and j['sw_keys'] == i:
      if fws[i].has_key('version'):
        if datetime.strptime(j['reldate'],'%Y/%m/%d') > datetime.strptime(fws[i]['version']['reldate'],'%Y/%m/%d'):
          fws[i]['version'] = j
      else:
        fws[i]['version'] = j

inv = open(os.path.join(fwdir, 'inventory'),"w")
inv.write('Firmware Inventory File\n')
inv.write('Updated %s\n\n' % datetime.strftime(datetime.today(),'%Y/%m/%d-%H:%M:%S'));

for i in fws:
  ddir=fwdir
  sw = fws[i]
  try:
    ver = sw['version']
  except KeyError:
    print "Warning: no Version informations found for %s" % i
    continue
  print
  print "--> Processing %s" % i
  print ver['name']
  if sw['type'] == 0:
    print "Auto Download Disabled!"
    print "Infos:"
    print " Filename: %s" % ver['filename']
    print " Url: %s" % ver['url']
    print " Ourname: %s" % sw['ourname'] if sw.has_key('ourname') else '-'
    continue
  elif sw['type'] == 2:
    ddir = os.path.join(ddir, 'disks')
  ensure_directory(ddir)
  filename = os.path.join(ddir, ver['filename'])
  if not os.path.exists(filename):
    print "Downloading %s" % filename
    if (download(filename, ver['url'])):
      print "Error: Download failed"
      continue
  updateinventory(inv, i)
  if sw.has_key('ourname'):
    link = os.path.join(ddir,sw['ourname'])
    if os.path.lexists(link): os.unlink(link)
    os.symlink(ver['filename'], link)
print "Finished."

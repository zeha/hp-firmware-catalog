import simplejson, os, subprocess

download_path = './downloads/'

catalog = simplejson.load(file('catalog.json','r'))
catalog_by_type = {}

for firmwareentry in catalog['entries']:
        if len(firmwareentry) < 1: continue
        sw_keys = firmwareentry['sw_keys']
        if not catalog_by_type.has_key(sw_keys):
                catalog_by_type[sw_keys] = []
        catalog_by_type[sw_keys].append(firmwareentry)

def ensure_directory(path):
        if not os.path.exists(path): os.mkdir(path)

ensure_directory(download_path)

for sw_key in catalog_by_type.keys():
        print "Checking firmware type %s" % sw_key
        swkey_path = os.path.join(download_path, sw_key.replace(' ','_'))
        ensure_directory(swkey_path)
        files_path = os.path.join(swkey_path, 'files')
        ensure_directory(files_path)

        for entry in catalog_by_type[sw_key]:
                filename = entry['filename']
                url = entry['url']
                reldate = entry['reldate']
                local_filename = os.path.join(files_path, filename)
                print "    Downloading %s" % filename

                curl_opts = ["curl","-f","-o",local_filename]
                if os.path.exists(local_filename):
                        curl_opts.append("-z")
                        curl_opts.append(local_filename)
                curl_opts.append(url)

                if subprocess.call(curl_opts) != 0:
                        print "    ...failed!"
                

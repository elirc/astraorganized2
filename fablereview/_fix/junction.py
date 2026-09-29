import subprocess, sys, os
cmd, link = sys.argv[1], sys.argv[2]
if cmd == 'make':
    target = sys.argv[3]
    if not os.path.lexists(link):
        r = subprocess.run(['cmd', '/c', 'mklink', '/J', link, target], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
elif cmd == 'drop':
    if os.path.lexists(link):
        subprocess.run(['cmd', '/c', 'rmdir', link])
        print('dropped', link)

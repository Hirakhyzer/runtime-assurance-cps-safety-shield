import hashlib,json,pathlib,subprocess,zlib
EXPECTED_LEN=29328
EXPECTED_SHA="dc0905af8a03467c876eed8bd6a486ac46738cd365709300e00c357b52552ef3"

def run(*args): subprocess.run(args,check=True)

def main():
    payload="".join(pathlib.Path(f".bootstrap_payload/part_{i:02d}.txt").read_text().strip() for i in range(8))
    if len(payload)!=EXPECTED_LEN: raise RuntimeError(f"payload length {len(payload)} != {EXPECTED_LEN}")
    comp=bytes.fromhex(payload)
    if hashlib.sha256(comp).hexdigest()!=EXPECTED_SHA: raise RuntimeError("payload sha256 mismatch")
    files=json.loads(zlib.decompress(comp).decode())
    for path,content in files.items():
        p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding="utf-8")
    import shutil
    shutil.rmtree(".bootstrap_payload")
    pathlib.Path("bootstrap_repo.py").unlink()
    pathlib.Path(".github/workflows/bootstrap.yml").unlink()
    run("git","config","user.name","github-actions[bot]")
    run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
    run("git","add","-A")
    run("git","commit","-m","Add runtime assurance CPS safety shield research framework")
    run("git","push","origin","HEAD:main")

if __name__=="__main__": main()

import sys, traceback, time
from build import build
nums=[int(x) for x in open("resto.txt").read().split()]
for n in nums:
    t=time.time()
    try:
        st=build(n)
        print(n, "libri:", len(st), "par:", sum(s[1] for s in st), "/", sum(s[2] for s in st),
              "non allineati:", sum(s[3] for s in st), "note:", sum(s[4] for s in st), f"{time.time()-t:.0f}s", flush=True)
    except Exception as e:
        print(n, "ERRORE", repr(e)[:200], flush=True); traceback.print_exc(file=sys.stderr)
print("FINE", flush=True)

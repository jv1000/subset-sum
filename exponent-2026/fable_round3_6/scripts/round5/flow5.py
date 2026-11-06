"""Round-5 library: collapsed (sparse) YP / YPQ / YPQx flow with a memory guard, and named Hall violators.

Sources (X, A, A') with supply N(A')/f(X) are merged by their rule key (YP: P; YPQ: (P, Q); YPQx: (P, Q, X) when X is
itself a collision set, else (P, Q)); targets (Y, Y*, D) are merged by Y with capacity cap(Y) = sum N(D)/f(Y).
A merged source is joined (infinite capacity) to Y iff the rule admits the edge.  Merging nodes with identical
neighbourhoods does not change the max-flow value, so the routed fraction equals that of the explicit flow of
../round4/charge_flow4.py (checked there on random cases)."""
import sys, os, ctypes
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "round4"))
sys.path.insert(0, os.path.join(HERE, "..", "round3"))
from collections import defaultdict
from charge_flow import Inst, pc
from lay3 import Dinic

EMAX = 3_000_000      # merged-edge cap per case
RSS_MAX_MB = 1500     # abort the run above this working set

class _PMC(ctypes.Structure):
    _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong)] + [(n, ctypes.c_size_t) for n in (
        "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
        "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]

_k32 = ctypes.windll.kernel32; _k32.GetCurrentProcess.restype = ctypes.c_void_p
_gpmi = ctypes.windll.psapi.GetProcessMemoryInfo; _gpmi.argtypes = [ctypes.c_void_p, ctypes.POINTER(_PMC), ctypes.c_ulong]

def rss_mb():
    pmc = _PMC(); pmc.cb = ctypes.sizeof(_PMC)
    if not _gpmi(_k32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb): raise OSError("GetProcessMemoryInfo failed")
    return pmc.WorkingSetSize / 2 ** 20

class MemoryGuard(Exception):
    pass

def guard():
    r = rss_mb()
    if r > RSS_MAX_MB: raise MemoryGuard(f"working set {r:.0f} MB > {RSS_MAX_MB} MB")
    return r

RULES = ("YP", "YPQx", "YPQ")

class Inst5(Inst):
    def __init__(self, w, t, k):
        super().__init__(w, t, k)
        self.capY = {Y: sum(self.tgt[(Y, Ys, D)] for Ys, D in self.byY[Y]) for Y in self.collY}
        self.collset = set(self.collY)

    def groups(self, rule):
        g = defaultdict(float)
        for X, A, A2, s in self.src:
            P = A & ~A2; Q = A2 & ~A
            if rule == "YP": key = (P, 0, -1)
            elif rule == "YPQ": key = (P, Q, -1)
            else: key = (P, Q, X if X in self.collset else -1)
            g[key] += s
        return g

    def admits(self, rule, key, Y):
        P, Q, Xx = key
        if Y == Xx: return False
        return (Y & P) == P or (rule != "YP" and (Y & Q) == Q)

    def flow(self, rule, SCALE=1 << 36, want_cut=False):
        """Returns (routed fraction or None if skipped by the edge cap, merged edge count[, Hall violator])."""
        g = self.groups(rule); keys = list(g); ng = len(keys); nY = len(self.collY)
        adj = [[j for j, Y in enumerate(self.collY) if self.admits(rule, key, Y)] for key in keys]
        ne = sum(map(len, adj))
        if ne > EMAX: return (None, ne, None) if want_cut else (None, ne)
        guard()
        D = Dinic(2 + ng + nY); S, T = 0, 1
        for i, key in enumerate(keys):
            D.add(S, 2 + i, int(g[key] * SCALE))
            for j in adj[i]: D.add(2 + i, 2 + ng + j, 1 << 62)
        for j, Y in enumerate(self.collY): D.add(2 + ng + j, T, int(self.capY[Y] * SCALE))
        fl = D.maxflow(S, T) / SCALE
        fr = fl / self.supply if self.supply > 0 else 1.0
        if not want_cut: return fr, ne
        # Hall violator: source classes reachable from S in the residual graph (D.lv >= 0 after the last failed BFS)
        D.bfs(S, T)
        R = [keys[i] for i in range(ng) if D.lv[2 + i] >= 0]
        Ys = [self.collY[j] for j in range(nY) if D.lv[2 + ng + j] >= 0]
        cut = {"groups": R, "supply": sum(g[k] for k in R), "Y": Ys, "cap": sum(self.capY[Y] for Y in Ys)}
        return fr, ne, cut

    def names(self, mask):
        return "{" + ",".join(str(self.w[e]) for e in range(self.m) if (mask >> e) & 1) + "}"

    def describe_cut(self, cut, limit=12):
        out = [f"Hall violator: {len(cut['groups'])} merged source classes, supply {cut['supply']:.4f}; "
               f"neighbourhood {len(cut['Y'])} collision sets, capacity {cut['cap']:.4f}"]
        for P, Q, Xx in cut["groups"][:limit]:
            out.append(f"   P={self.names(P)}" + (f" Q={self.names(Q)}" if Q else "") + (f" X={self.names(Xx)}" if Xx >= 0 else ""))
        for Y in cut["Y"][:limit]: out.append(f"   Y={self.names(Y)} f={self.f[Y]} cap={self.capY[Y]:.4f}")
        return "\n".join(out)

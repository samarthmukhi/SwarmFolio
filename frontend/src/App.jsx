import { useState, useEffect, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { ThinkingOrb } from "thinking-orbs"
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine,
} from "recharts"

/* ---------- Brand icons ---------- */
const iconCls = "h-5 w-5"
function GitHubIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={iconCls} aria-hidden="true">
      <path d="M12 .5C5.37.5 0 5.78 0 12.29c0 5.2 3.44 9.6 8.21 11.16.6.11.82-.25.82-.56 0-.28-.01-1.02-.02-2C5.67 21.7 4.97 19.7 4.97 19.7c-.55-1.36-1.34-1.72-1.34-1.72-1.1-.73.08-.72.08-.72 1.21.08 1.84 1.22 1.84 1.22 1.08 1.8 2.81 1.28 3.5.98.11-.76.42-1.28.76-1.57-2.66-.29-5.47-1.29-5.47-5.75 0-1.27.47-2.3 1.24-3.12-.13-.29-.54-1.47.12-3.06 0 0 1.01-.32 3.3 1.19a11.6 11.6 0 0 1 3-.39c1.02 0 2.05.13 3 .39 2.28-1.51 3.29-1.19 3.29-1.19.66 1.59.24 2.77.12 3.06.77.82 1.24 1.85 1.24 3.12 0 4.47-2.81 5.45-5.49 5.74.43.36.81 1.07.81 2.16 0 1.56-.01 2.82-.01 3.2 0 .31.22.68.83.56A11.8 11.8 0 0 0 24 12.29C24 5.78 18.63.5 12 .5z" />
    </svg>
  )
}
function LinkedInIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={iconCls} aria-hidden="true">
      <path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z" />
    </svg>
  )
}
function GlobeIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" className={iconCls} aria-hidden="true">
      <circle cx="12" cy="12" r="9" />
      <line x1="3" y1="12" x2="21" y2="12" />
      <path d="M12 3a15 15 0 0 1 4 9 15 15 0 0 1-4 9 15 15 0 0 1-4-9 15 15 0 0 1 4-9z" />
    </svg>
  )
}

/* ---------- Background: a visible drifting particle swarm (monochrome) ---------- */
function SwarmBackground() {
  const ref = useRef(null)
  useEffect(() => {
    const canvas = ref.current
    const ctx = canvas.getContext("2d")
    let w, h, raf
    const dpr = Math.min(window.devicePixelRatio || 1, 2)
    function resize() {
      w = canvas.width = window.innerWidth * dpr
      h = canvas.height = window.innerHeight * dpr
      canvas.style.width = window.innerWidth + "px"
      canvas.style.height = window.innerHeight + "px"
    }
    resize()
    const N = 90
    const p = Array.from({ length: N }, () => ({
      x: Math.random() * w, y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.25 * dpr, vy: (Math.random() - 0.5) * 0.25 * dpr,
      r: (Math.random() * 2 + 1.3) * dpr,
    }))
    const LINK = 145 * dpr
    function tick() {
      ctx.clearRect(0, 0, w, h)
      // links
      ctx.shadowBlur = 0
      for (let i = 0; i < N; i++) {
        const a = p[i]
        for (let j = i + 1; j < N; j++) {
          const b = p[j]
          const dx = a.x - b.x, dy = a.y - b.y
          const d = Math.hypot(dx, dy)
          if (d < LINK) {
            ctx.strokeStyle = `rgba(255,255,255,${0.12 * (1 - d / LINK)})`
            ctx.lineWidth = dpr
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke()
          }
        }
      }
      // dots (with glow)
      ctx.shadowBlur = 4 * dpr
      ctx.shadowColor = "rgba(255,255,255,0.28)"
      ctx.fillStyle = "rgba(255,255,255,0.42)"
      for (let i = 0; i < N; i++) {
        const a = p[i]
        a.x += a.vx; a.y += a.vy
        if (a.x < 0 || a.x > w) a.vx *= -1
        if (a.y < 0 || a.y > h) a.vy *= -1
        ctx.beginPath()
        ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2)
        ctx.fill()
      }
      raf = requestAnimationFrame(tick)
    }
    tick()
    window.addEventListener("resize", resize)
    return () => { cancelAnimationFrame(raf); window.removeEventListener("resize", resize) }
  }, [])
  return <canvas ref={ref} className="pointer-events-none fixed inset-0 -z-10" />
}

/* ---------- Mock data (until we wire the real engine) ---------- */
const MOCK_EQUITY = (() => {
  const pts = []; let v = 1
  for (let i = 0; i <= 120; i++) {
    v *= 1 + 0.017 + Math.sin(i / 5) * 0.018 + Math.cos(i / 11) * 0.01
    pts.push({ t: 2016 + i / 12, value: +v.toFixed(3) })
  }
  return pts
})()

const MOCK_RESULT = {
  feasible: true,
  sharpe: 1.38,
  annual_return: 0.241,
  max_drawdown: -0.223,
  holdings: [
    { ticker: "GLD", weight: 0.345 }, { ticker: "NVDA", weight: 0.291 },
    { ticker: "WMT", weight: 0.136 }, { ticker: "JNJ", weight: 0.12 },
    { ticker: "JPM", weight: 0.072 }, { ticker: "AMZN", weight: 0.036 },
  ],
  equity: MOCK_EQUITY,
}

/* ---------- UI helpers ---------- */
function Panel({ children, className = "" }) {
  return (
    <div className={`rounded-xl border border-neutral-800 bg-neutral-950/60 backdrop-blur-sm transition-colors duration-300 hover:border-neutral-700 ${className}`}>
      {children}
    </div>
  )
}
function Metric({ label, value, tone = "white" }) {
  const color = tone === "green" ? "text-emerald-400" : tone === "red" ? "text-rose-400" : "text-white"
  return (
    <Panel className="p-5">
      <div className="text-[11px] uppercase tracking-[0.2em] text-neutral-500">{label}</div>
      <div className={`mt-2 text-3xl font-medium ${color}`}>{value}</div>
    </Panel>
  )
}
function Slider({ label, value, setValue, min, max, suffix = "" }) {
  return (
    <div>
      <div className="mb-3 flex items-center justify-between">
        <span className="text-sm text-neutral-400">{label}</span>
        <span className="text-sm font-medium text-white tabular-nums">{value}{suffix}</span>
      </div>
      <input type="range" min={min} max={max} value={value}
        onChange={(e) => setValue(Number(e.target.value))} />
    </div>
  )
}

/* ---------- Loading stages (orb state + live status message) ---------- */
const STAGES = [
  { msg: "Initializing swarm", orb: "working" },
  { msg: "Scattering 50 particles", orb: "connecting" },
  { msg: "Weaving candidate allocations", orb: "weaving" },
  { msg: "Searching for the optimum", orb: "searching" },
  { msg: "Checking feasibility", orb: "solving" },
  { msg: "Finalizing allocation", orb: "shaping" },
]

/* ---------- Main app ---------- */
export default function App() {
  const [maxHoldings, setMaxHoldings] = useState(8)
  const [minWeight, setMinWeight] = useState(5)
  const [minHoldings, setMinHoldings] = useState(3)
  const [loading, setLoading] = useState(false)
  const [stage, setStage] = useState(0)
  const [result, setResult] = useState(null)

  const orbState = loading ? STAGES[stage].orb : "breathing"

  async function handleOptimize() {
    setLoading(true)
    setResult(null)
    setStage(0)

    // walk through the status stages for a deliberate, trustworthy pace
    let s = 0
    const interval = setInterval(() => {
      s = Math.min(s + 1, STAGES.length - 1)
      setStage(s)
    }, 1000)

    // the real work + a minimum on-screen duration, whichever is longer
    const minDuration = new Promise((r) => setTimeout(r, STAGES.length * 1000 + 400))
    const fetchData = fetch(`${import.meta.env.VITE_API_URL || ""}/optimize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        max_holdings: maxHoldings,
        min_weight: minWeight / 100, // % -> fraction
        min_holdings: minHoldings,
      }),
    })
      .then((r) => { if (!r.ok) throw new Error("bad response"); return r.json() })
      .catch(() => ({ error: true }))

    const [data] = await Promise.all([fetchData, minDuration])
    clearInterval(interval)
    setResult(data)
    setLoading(false)
  }

  return (
    <div className="relative min-h-screen w-full text-neutral-200">
      <SwarmBackground />

      <div className="mx-auto flex min-h-screen max-w-3xl flex-col px-6 py-20">
        {/* Hero */}
        <div className="flex flex-col items-center text-center">
          <div style={{ transform: "scale(1.6)" }} className="mb-10">
            <ThinkingOrb state={orbState} size={64} theme="dark" />
          </div>
          <div className="text-xs font-medium tracking-[0.4em] text-neutral-500">SWARMFOLIO</div>
          <h1 className="mt-4 text-4xl font-medium tracking-tight text-white md:text-5xl">
            Portfolios, found by a swarm.
          </h1>
          <p className="mt-4 max-w-md text-[15px] leading-relaxed text-neutral-500">
            Particle swarm optimization for constrained portfolios — and an honest answer when none exists.
          </p>
        </div>

        {/* Control panel */}
        <Panel className="mt-14 p-7">
          <div className="grid gap-7 md:grid-cols-3">
            <Slider label="Max holdings" value={maxHoldings} setValue={setMaxHoldings} min={2} max={19} />
            <Slider label="Min position" value={minWeight} setValue={setMinWeight} min={0} max={25} suffix="%" />
            <Slider label="Min holdings" value={minHoldings} setValue={setMinHoldings} min={0} max={12} />
          </div>
          <motion.button
            onClick={handleOptimize} disabled={loading}
            whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.985 }}
            className="mt-8 w-full rounded-lg bg-white px-6 py-3.5 text-sm font-medium tracking-wide text-black transition-shadow duration-300 hover:shadow-[0_0_28px_rgba(255,255,255,0.25)] disabled:cursor-not-allowed disabled:opacity-40 disabled:shadow-none"
          >
            {loading ? "Swarming…" : "Optimize portfolio"}
          </motion.button>
        </Panel>

        {/* Loading */}
        <AnimatePresence mode="wait">
          {loading && (
            <motion.div key={stage}
              initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.3 }}
              className="mt-10 flex items-center justify-center gap-2.5 text-sm text-neutral-400">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-white" />
              {STAGES[stage].msg}…
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error */}
        <AnimatePresence>
          {result?.error && !loading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="mt-10 text-center text-sm text-neutral-400">
              Couldn't reach the engine — is the API server running on :8000?
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {result && !result.error && !loading && (
            <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}
              className="mt-12 space-y-6">
              <div className="flex items-center gap-2.5 text-sm">
                <span className={`h-1.5 w-1.5 rounded-full ${result.feasible ? "bg-white" : "border border-neutral-500"}`} />
                <span className={result.feasible ? "text-white" : "text-neutral-500"}>
                  {result.feasible ? "Feasible allocation found" : "No allocation satisfies these constraints"}
                </span>
              </div>

              <div className="grid gap-4 sm:grid-cols-3">
                <Metric label="Sharpe" value={result.sharpe.toFixed(2)} />
                <Metric label="Annual return" value={`${(result.annual_return * 100).toFixed(0)}%`} tone="green" />
                <Metric label="Max drawdown" value={`${(result.max_drawdown * 100).toFixed(0)}%`} tone="red" />
              </div>

              <Panel className="p-6">
                <h2 className="mb-5 text-sm font-medium uppercase tracking-[0.15em] text-neutral-500">Allocation</h2>
                <div className="space-y-4">
                  {result.holdings.map((h) => (
                    <div key={h.ticker}>
                      <div className="mb-1.5 flex justify-between text-sm">
                        <span className="font-medium text-white">{h.ticker}</span>
                        <span className="text-neutral-500 tabular-nums">{(h.weight * 100).toFixed(1)}%</span>
                      </div>
                      <div className="h-[3px] overflow-hidden rounded-full bg-neutral-900">
                        <motion.div className="h-full rounded-full bg-white"
                          initial={{ width: 0 }} animate={{ width: `${h.weight * 100}%` }}
                          transition={{ duration: 0.7, ease: "easeOut" }} />
                      </div>
                    </div>
                  ))}
                </div>
              </Panel>

              <Panel className="p-6">
                <div className="mb-5 flex items-center justify-between">
                  <h2 className="text-sm font-medium uppercase tracking-[0.15em] text-neutral-500">Backtest — $1 over time</h2>
                  <span className="text-sm font-medium tabular-nums text-emerald-400">
                    +{((result.equity[result.equity.length - 1].value - 1) * 100).toFixed(0)}%
                  </span>
                </div>
                <ResponsiveContainer width="100%" height={240}>
                  <AreaChart data={result.equity} margin={{ top: 6, right: 6, left: -14, bottom: 0 }}>
                    <defs>
                      <linearGradient id="eqUp" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#22c55e" stopOpacity={0.35} />
                        <stop offset="100%" stopColor="#22c55e" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                    <XAxis dataKey="t" type="number" domain={["dataMin", "dataMax"]}
                      ticks={[2016, 2018, 2020, 2022, 2024, 2026]} tickFormatter={(v) => `'${String(Math.round(v)).slice(2)}`}
                      tick={{ fill: "#737373", fontSize: 11 }} axisLine={{ stroke: "#262626" }} tickLine={false} />
                    <YAxis tickFormatter={(v) => `$${v}`} domain={[0, "auto"]}
                      tick={{ fill: "#737373", fontSize: 11 }} axisLine={false} tickLine={false} width={40} />
                    <Tooltip contentStyle={{ background: "#0a0a0a", border: "1px solid #262626", borderRadius: 8 }}
                      itemStyle={{ color: "#22c55e" }} labelStyle={{ color: "#a3a3a3" }}
                      formatter={(v) => [`$${v}`, "Value"]} labelFormatter={(v) => `'${String(Math.round(v)).slice(2)}`} />
                    <ReferenceLine y={1} stroke="#ef4444" strokeDasharray="4 4" strokeOpacity={0.55}
                      label={{ value: "break-even", fill: "#ef4444", fontSize: 10, position: "insideBottomRight", opacity: 0.7 }} />
                    <Area type="monotone" dataKey="value" stroke="#22c55e" strokeWidth={2} fill="url(#eqUp)" />
                  </AreaChart>
                </ResponsiveContainer>
              </Panel>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        <footer className="mt-auto pt-24 text-center">
          <div className="border-t border-neutral-900 pt-8">
            <div className="text-sm text-neutral-500">
              Built by <span className="text-neutral-200">Samarth Mukhi</span>
            </div>
            <div className="mt-4 flex items-center justify-center gap-7">
              {[
                { label: "Website", href: "https://samarthmukhi.com", icon: <GlobeIcon /> },
                { label: "GitHub", href: "https://github.com/samarthmukhi", icon: <GitHubIcon /> },
                { label: "LinkedIn", href: "https://linkedin.com/in/samarthmukhi", icon: <LinkedInIcon /> },
              ].map((l) => (
                <a key={l.label} href={l.href} target="_blank" rel="noreferrer" aria-label={l.label}
                  className="text-neutral-500 transition-all duration-200 hover:-translate-y-0.5 hover:text-white">
                  {l.icon}
                </a>
              ))}
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}

import { NavLink, Outlet } from 'react-router-dom'
import { useEffect, useState } from 'react'

export default function Layout() {
  const [online, setOnline] = useState<boolean | null>(null)

  useEffect(() => {
    fetch('/healthz')
      .then(r => r.ok ? setOnline(true) : setOnline(false))
      .catch(() => setOnline(false))
  }, [])

  const navClass = ({ isActive }: { isActive: boolean }) =>
    `px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
      isActive
        ? 'bg-sky-500 text-white'
        : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800'
    }`

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-4">
          <div className="flex items-center gap-2 mr-4">
            <span className="text-sky-400 font-bold text-lg">SyncSenta</span>
            <span className="text-xs bg-emerald-900/60 text-emerald-400 px-2 py-0.5 rounded-full border border-emerald-800">
              Education OS
            </span>
          </div>

          <nav className="flex items-center gap-1">
            <NavLink to="/" end className={navClass}>Home</NavLink>
            <NavLink to="/tutor" className={navClass}>AI Tutor</NavLink>
            <NavLink to="/quiz" className={navClass}>Quiz</NavLink>
          </nav>

          <div className="ml-auto flex items-center gap-2 text-xs text-slate-500">
            <span
              className={`w-2 h-2 rounded-full ${
                online === null ? 'bg-slate-600 animate-pulse' :
                online ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'
              }`}
            />
            {online === null ? 'Connecting…' : online ? 'AI Online' : 'API Offline'}
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-5xl mx-auto w-full px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}

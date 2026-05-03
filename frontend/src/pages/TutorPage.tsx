import { useState, useRef, useEffect } from 'react'

interface Message {
  id: string
  role: 'user' | 'agent'
  text: string
  agentName?: string
  loading?: boolean
}

const GRADES = ['Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8']
const SUBJECTS = ['Mathematics', 'Science', 'English', 'Kiswahili', 'Social Studies']
const LANGUAGES = [{ value: 'english', label: 'English' }, { value: 'swahili', label: 'Kiswahili' }]

export default function TutorPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'agent',
      agentName: 'SyncSenta AI Tutor',
      text: 'Habari! I\'m your CBC-aligned AI tutor. Ask me anything about your school subjects — I\'ll guide you step by step using examples from everyday Kenyan life!',
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [grade, setGrade] = useState('Grade 4')
  const [subject, setSubject] = useState('Mathematics')
  const [language, setLanguage] = useState('english')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function send() {
    const text = input.trim()
    if (!text || loading) return
    setInput('')

    const userMsg: Message = { id: Date.now().toString(), role: 'user', text }
    const loadingMsg: Message = { id: 'loading', role: 'agent', text: '', loading: true, agentName: 'AI Tutor' }
    setMessages(prev => [...prev, userMsg, loadingMsg])
    setLoading(true)

    try {
      const res = await fetch('/agents/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, grade, subject, language, role: 'student', user_id: 'demo-user' }),
      })
      const data = await res.json()
      setMessages(prev => [
        ...prev.filter(m => m.id !== 'loading'),
        {
          id: Date.now().toString(),
          role: 'agent',
          agentName: data.primary_agent ?? 'AI Tutor',
          text: data.response ?? data.detail ?? 'Sorry, I could not process that.',
        },
      ])
    } catch {
      setMessages(prev => [
        ...prev.filter(m => m.id !== 'loading'),
        { id: Date.now().toString(), role: 'agent', agentName: 'System', text: 'Connection error — please try again.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
        <h1 className="text-sky-400 font-semibold mb-4">AI Tutor — Mwalimu Agent</h1>

        <div className="grid grid-cols-3 gap-3 mb-4">
          <label className="flex flex-col gap-1">
            <span className="text-xs text-slate-500">Grade</span>
            <select
              value={grade}
              onChange={e => setGrade(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-sky-500"
            >
              {GRADES.map(g => <option key={g}>{g}</option>)}
            </select>
          </label>
          <label className="flex flex-col gap-1">
            <span className="text-xs text-slate-500">Subject</span>
            <select
              value={subject}
              onChange={e => setSubject(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-sky-500"
            >
              {SUBJECTS.map(s => <option key={s}>{s}</option>)}
            </select>
          </label>
          <label className="flex flex-col gap-1">
            <span className="text-xs text-slate-500">Language</span>
            <select
              value={language}
              onChange={e => setLanguage(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-sky-500"
            >
              {LANGUAGES.map(l => <option key={l.value} value={l.value}>{l.label}</option>)}
            </select>
          </label>
        </div>

        <div className="h-80 overflow-y-auto scrollbar-thin flex flex-col gap-3 bg-slate-950 rounded-xl p-4 mb-3">
          {messages.map(m => (
            <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-[78%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  m.role === 'user'
                    ? 'bg-sky-500 text-white rounded-br-sm'
                    : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-bl-sm'
                }`}
              >
                {m.role === 'agent' && m.agentName && (
                  <p className="text-sky-400 text-xs font-semibold mb-1">{m.agentName}</p>
                )}
                {m.loading ? (
                  <span className="flex gap-1 items-center">
                    <span className="w-1.5 h-1.5 bg-sky-400 rounded-full animate-bounce [animation-delay:0ms]" />
                    <span className="w-1.5 h-1.5 bg-sky-400 rounded-full animate-bounce [animation-delay:150ms]" />
                    <span className="w-1.5 h-1.5 bg-sky-400 rounded-full animate-bounce [animation-delay:300ms]" />
                  </span>
                ) : (
                  m.text
                )}
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        <div className="flex gap-2">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && send()}
            placeholder="Ask a question about any CBC subject…"
            className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder:text-slate-600 outline-none focus:border-sky-500"
          />
          <button
            onClick={send}
            disabled={loading || !input.trim()}
            className="px-5 py-2.5 bg-sky-500 hover:bg-sky-600 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-xl text-sm font-semibold transition-colors"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  )
}

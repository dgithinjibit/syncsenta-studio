import { Link } from 'react-router-dom'

const features = [
  {
    icon: '🤖',
    title: 'AI Tutor',
    desc: 'Socratic-style tutoring in English and Swahili using CBC curriculum context. Local examples — shillings, matatu, chapati.',
    href: '/tutor',
    cta: 'Start Learning',
  },
  {
    icon: '📝',
    title: 'Quiz Generator',
    desc: 'Auto-generate CBC-aligned quizzes with KICD strand citations for any grade and subject. Instant grading with rubric feedback.',
    href: '/quiz',
    cta: 'Generate Quiz',
  },
  {
    icon: '📊',
    title: 'Assessment & Grading',
    desc: 'Rubric-based grading of short answers and MCQs, with competency tracking aligned to Kenya National Exam standards.',
    href: '/quiz',
    cta: 'Try Assessment',
  },
  {
    icon: '🌍',
    title: 'Kenya-First Context',
    desc: 'Every response is grounded in Kenyan culture. Built for CBC curriculum, KICD strands, and real classroom needs.',
    href: '/tutor',
    cta: 'Explore',
  },
]

const stack = [
  { label: 'Frontend', value: 'React + TypeScript + Vite + Tailwind' },
  { label: 'AI Agents', value: 'LangChain + LangGraph (offline-first)' },
  { label: 'Backend', value: 'Python FastAPI + Rust/Axum' },
  { label: 'Blockchain', value: 'Polygon (Solidity smart contracts)' },
  { label: 'Curriculum', value: 'Kenya CBC / KICD-aligned' },
]

export default function HomePage() {
  return (
    <div className="space-y-12">
      <section className="text-center py-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-sky-400 to-indigo-400 bg-clip-text text-transparent mb-4">
          Kenya's CBC Education Platform
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          AI-powered learning tools for students, teachers, and schools — offline-first,
          decentralised, built for 100,000+ concurrent users.
        </p>
        <div className="flex justify-center gap-3 mt-6">
          <Link
            to="/tutor"
            className="px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white rounded-xl font-semibold transition-colors"
          >
            Try AI Tutor
          </Link>
          <Link
            to="/quiz"
            className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-slate-100 rounded-xl font-semibold transition-colors border border-slate-700"
          >
            Generate Quiz
          </Link>
        </div>
      </section>

      <section className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {features.map(f => (
          <div key={f.title} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 hover:border-slate-700 transition-colors">
            <div className="text-3xl mb-3">{f.icon}</div>
            <h3 className="text-sky-400 font-semibold text-base mb-2">{f.title}</h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-4">{f.desc}</p>
            <Link
              to={f.href}
              className="text-sm text-sky-400 hover:text-sky-300 font-medium transition-colors"
            >
              {f.cta} →
            </Link>
          </div>
        ))}
      </section>

      <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Tech Stack</h2>
        <div className="space-y-2">
          {stack.map(s => (
            <div key={s.label} className="flex items-start gap-4 text-sm">
              <span className="text-slate-500 w-24 shrink-0">{s.label}</span>
              <span className="text-slate-300">{s.value}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

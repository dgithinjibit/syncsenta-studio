import { useState } from 'react'

interface Question {
  question: string
  question_type: 'multiple_choice' | 'true_false' | 'short_answer'
  options: string[]
  correct_answer: string
  difficulty: string
  points: number
  competency?: string
  cbc_citation?: string
}

interface Quiz {
  title: string
  competencies: string[]
  cbc_citations: string[]
  questions: Question[]
}

interface GradeResult {
  total_points_earned: number
  total_points_possible: number
  overall_feedback?: { overall_feedback?: string; next_steps?: string[] }
  graded_answers?: { correct: boolean; points_earned: number; feedback?: string }[]
}

const GRADES = [{ value: 'g4', label: 'Grade 4' }, { value: 'g5', label: 'Grade 5' }, { value: 'g6', label: 'Grade 6' }, { value: 'g7', label: 'Grade 7' }]
const SUBJECTS = ['Mathematics', 'Science', 'English', 'Social Studies']

export default function QuizPage() {
  const [grade, setGrade] = useState('g4')
  const [subject, setSubject] = useState('Mathematics')
  const [competency, setCompetency] = useState('fractions')
  const [numQuestions, setNumQuestions] = useState('5')
  const [generating, setGenerating] = useState(false)
  const [quiz, setQuiz] = useState<Quiz | null>(null)
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [gradeResult, setGradeResult] = useState<GradeResult | null>(null)
  const [grading, setGrading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function generate() {
    setGenerating(true)
    setQuiz(null)
    setGradeResult(null)
    setAnswers({})
    setError(null)
    try {
      const res = await fetch('/agents/assessment/quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grade, subject, competency, num_questions: parseInt(numQuestions), language: 'english' }),
      })
      if (!res.ok) throw new Error(await res.text())
      setQuiz(await res.json())
    } catch (e) {
      setError(String(e))
    } finally {
      setGenerating(false)
    }
  }

  async function submitQuiz() {
    if (!quiz) return
    setGrading(true)
    try {
      const submission = {
        quiz_id: 'demo',
        student_id: 'demo-student',
        answers: quiz.questions.map((_, i) => ({ question_id: String(i), answer: answers[i] ?? '' })),
      }
      const res = await fetch('/agents/assessment/grade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quiz, submission }),
      })
      if (!res.ok) throw new Error(await res.text())
      setGradeResult(await res.json())
    } catch (e) {
      setError(String(e))
    } finally {
      setGrading(false)
    }
  }

  const diffColor = (d: string) =>
    d === 'easy' ? 'bg-emerald-900/50 text-emerald-400 border-emerald-800' :
    d === 'hard' ? 'bg-red-900/50 text-red-400 border-red-800' :
    'bg-amber-900/50 text-amber-400 border-amber-800'

  const pct = gradeResult
    ? Math.round((gradeResult.total_points_earned / (gradeResult.total_points_possible || 1)) * 100)
    : null

  return (
    <div className="space-y-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
        <h1 className="text-sky-400 font-semibold mb-4">CBC Quiz Generator</h1>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <label className="flex flex-col gap-1">
            <span className="text-xs text-slate-500">Grade</span>
            <select value={grade} onChange={e => setGrade(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-sky-500">
              {GRADES.map(g => <option key={g.value} value={g.value}>{g.label}</option>)}
            </select>
          </label>
          <label className="flex flex-col gap-1">
            <span className="text-xs text-slate-500">Subject</span>
            <select value={subject} onChange={e => setSubject(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-sky-500">
              {SUBJECTS.map(s => <option key={s}>{s}</option>)}
            </select>
          </label>
          <label className="flex flex-col gap-1">
            <span className="text-xs text-slate-500">Topic / Competency</span>
            <input value={competency} onChange={e => setCompetency(e.target.value)}
              placeholder="e.g. fractions"
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-sky-500" />
          </label>
          <label className="flex flex-col gap-1">
            <span className="text-xs text-slate-500">Questions</span>
            <select value={numQuestions} onChange={e => setNumQuestions(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-sky-500">
              {['3', '5', '10'].map(n => <option key={n}>{n}</option>)}
            </select>
          </label>
        </div>
        <button onClick={generate} disabled={generating}
          className="mt-4 px-6 py-2.5 bg-sky-500 hover:bg-sky-600 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-xl text-sm font-semibold transition-colors">
          {generating ? 'Generating…' : 'Generate Quiz'}
        </button>
        {error && <p className="mt-3 text-red-400 text-sm">{error}</p>}
      </div>

      {quiz && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-5">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">{quiz.title}</h2>
            {quiz.cbc_citations?.length > 0 && (
              <p className="text-xs text-slate-500 mt-1">📚 {quiz.cbc_citations.join(' · ')}</p>
            )}
          </div>

          {quiz.questions.map((q, i) => {
            const ga = gradeResult?.graded_answers?.[i]
            return (
              <div key={i} className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                <div className="flex items-start gap-3 mb-3">
                  <span className="text-sky-400 font-semibold text-sm shrink-0">Q{i + 1}</span>
                  <p className="text-slate-200 text-sm leading-relaxed flex-1">{q.question}</p>
                  <span className={`text-xs px-2 py-0.5 rounded-full border shrink-0 ${diffColor(q.difficulty)}`}>
                    {q.difficulty}
                  </span>
                </div>

                {q.question_type === 'short_answer' ? (
                  <input
                    value={answers[i] ?? ''}
                    onChange={e => setAnswers(prev => ({ ...prev, [i]: e.target.value }))}
                    disabled={!!gradeResult}
                    placeholder="Type your answer…"
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-sky-500 disabled:opacity-60"
                  />
                ) : (
                  <div className="grid gap-2">
                    {q.options.map((opt, oi) => {
                      const isSelected = answers[i] === opt
                      const isCorrect = gradeResult && opt === q.correct_answer
                      const isWrong = gradeResult && isSelected && opt !== q.correct_answer
                      return (
                        <button key={oi} disabled={!!gradeResult}
                          onClick={() => setAnswers(prev => ({ ...prev, [i]: opt }))}
                          className={`text-left px-4 py-2.5 rounded-lg text-sm border transition-all ${
                            isCorrect ? 'border-emerald-500 bg-emerald-900/40 text-emerald-300' :
                            isWrong ? 'border-red-500 bg-red-900/40 text-red-300' :
                            isSelected ? 'border-sky-500 bg-sky-900/40 text-sky-200' :
                            'border-slate-700 text-slate-300 hover:border-slate-500 disabled:cursor-default'
                          }`}>
                          {opt}
                        </button>
                      )
                    })}
                  </div>
                )}

                {ga && (
                  <p className={`mt-2 text-xs ${ga.correct ? 'text-emerald-400' : 'text-red-400'}`}>
                    {ga.correct ? '✓ Correct' : '✗ Incorrect'} — {ga.points_earned}/{q.points} pts
                    {ga.feedback ? ` · ${ga.feedback}` : ''}
                  </p>
                )}
              </div>
            )
          })}

          {!gradeResult && (
            <button onClick={submitQuiz} disabled={grading}
              className="px-6 py-2.5 bg-indigo-500 hover:bg-indigo-600 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-xl text-sm font-semibold transition-colors">
              {grading ? 'Grading…' : 'Submit Quiz'}
            </button>
          )}

          {gradeResult && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
              <h3 className="text-sky-400 font-semibold mb-3">Results</h3>
              <div className="text-4xl font-bold text-center text-sky-400 my-3">
                {gradeResult.total_points_earned}/{gradeResult.total_points_possible}
                <span className="text-2xl text-slate-400 ml-2">({pct}%)</span>
              </div>
              {gradeResult.overall_feedback?.overall_feedback && (
                <p className="text-slate-300 text-sm leading-relaxed mb-3">
                  {gradeResult.overall_feedback.overall_feedback}
                </p>
              )}
              {(gradeResult.overall_feedback?.next_steps ?? []).length > 0 && (
                <ul className="space-y-1">
                  {gradeResult.overall_feedback!.next_steps!.map((s, i) => (
                    <li key={i} className="text-emerald-400 text-sm">→ {s}</li>
                  ))}
                </ul>
              )}
              <button onClick={() => { setQuiz(null); setGradeResult(null); setAnswers({}) }}
                className="mt-4 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg text-sm transition-colors">
                Try Another Quiz
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

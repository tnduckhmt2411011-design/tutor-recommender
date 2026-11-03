import { useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'motion/react'
import ResultPage from './pages/ResultPage'
import SearchPage from './pages/SearchPage'
import {
  DEFAULT_PRIORITIES,
  buildRecommendationPayload,
  fetchRecommendations,
} from './services/api'
import './App.css'

function App() {
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('tutor_theme') || 'dark'
    } catch {
      return 'dark'
    }
  })

  useEffect(() => {
    try {
      document.documentElement.setAttribute('data-theme', theme)
      localStorage.setItem('tutor_theme', theme)
    } catch {
      // fallback
    }
  }, [theme])

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'))
  }

  const [searchForm, setSearchForm] = useState({
    subject: 'Toán',
    learningMode: 'in_person',
    preferredDistrict: 'Bình Thạnh',
    maxBudgetVnd: '200000',
    timeSlots: ['T2-tối', 'T4-tối'],
    priorities: { ...DEFAULT_PRIORITIES },
    topK: 3,
    scenarioMeta: null,
  })

  const [activeTab, setActiveTab] = useState('search')
  const [recommendationResult, setRecommendationResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [apiError, setApiError] = useState('')
  const [latencyMs, setLatencyMs] = useState(null)
  const [rankDeltas, setRankDeltas] = useState({})

  const requestSeqRef = useRef(0)

  const executeRecommendationRequest = async (
    nextFormState,
    options = { switchToResult: true, trackDeltaFrom: null }
  ) => {
    const seq = ++requestSeqRef.current
    const payload = buildRecommendationPayload(nextFormState)

    setIsLoading(true)
    setApiError('')

    if (options.switchToResult) {
      setRecommendationResult(null)
      setActiveTab('result')
    }

    const startTime = performance.now()
    try {
      const fetchPromise = fetchRecommendations(payload)
      const minDelayPromise = options.switchToResult
        ? new Promise((r) => setTimeout(r, 650))
        : Promise.resolve()
      const [responseData] = await Promise.all([fetchPromise, minDelayPromise])

      if (seq !== requestSeqRef.current) {
        return
      }
      const elapsed = performance.now() - startTime
      setLatencyMs(elapsed)

      if (
        options.trackDeltaFrom &&
        Array.isArray(options.trackDeltaFrom.results) &&
        Array.isArray(responseData.results)
      ) {
        const prevRankMap = Object.fromEntries(
          options.trackDeltaFrom.results.map((r) => [r.tutor_id, r.rank])
        )
        const nextDeltas = {}
        for (const item of responseData.results) {
          if (prevRankMap[item.tutor_id] !== undefined) {
            nextDeltas[item.tutor_id] = prevRankMap[item.tutor_id] - item.rank
          }
        }
        setRankDeltas(nextDeltas)
      } else {
        setRankDeltas({})
      }

      setRecommendationResult(responseData)
    } catch (error) {
      if (seq !== requestSeqRef.current) {
        return
      }
      setApiError(
        error instanceof Error
          ? error.message
          : 'Đã xảy ra lỗi khi gửi yêu cầu tới máy chủ gợi ý gia sư.'
      )
    } finally {
      if (seq === requestSeqRef.current) {
        setIsLoading(false)
      }
    }
  }

  const handleSubmitSearch = (formState) => {
    executeRecommendationRequest(formState, {
      switchToResult: true,
      trackDeltaFrom: null,
    })
  }

  const handleApplyScenario = (scenario) => {
    const nextForm = {
      subject: scenario.request.subject,
      learningMode: scenario.request.learning_mode,
      preferredDistrict: scenario.request.preferred_district || '',
      maxBudgetVnd:
        scenario.request.max_budget_vnd !== undefined &&
        scenario.request.max_budget_vnd !== null &&
        scenario.request.max_budget_vnd !== ''
          ? String(scenario.request.max_budget_vnd)
          : '',
      timeSlots: Array.isArray(scenario.request.time_slots)
        ? [...scenario.request.time_slots]
        : [],
      priorities: {
        ...DEFAULT_PRIORITIES,
        ...(scenario.request.priorities || {}),
      },
      topK: 3,
      scenarioMeta: scenario,
    }
    setSearchForm(nextForm)
    executeRecommendationRequest(nextForm, {
      switchToResult: true,
      trackDeltaFrom: null,
    })
  }

  const handleUpdatePrioritiesLive = (nextPriorities) => {
    const nextForm = {
      ...searchForm,
      priorities: nextPriorities,
    }
    setSearchForm(nextForm)
    executeRecommendationRequest(nextForm, {
      switchToResult: false,
      trackDeltaFrom: recommendationResult,
    })
  }

  return (
    <main className="app-container">
      <nav className="workflow-nav" aria-label="Điều hướng các bước khuyến nghị">
        <div className="workflow-tabs-group">
          <button
            type="button"
            className={`workflow-tab ${activeTab === 'search' ? 'active' : ''}`}
            onClick={() => setActiveTab('search')}
          >
            <span className="step-num">1</span>
            <span>Nhập nhu cầu & Trọng số (CN01)</span>
          </button>

          <button
            type="button"
            className={`workflow-tab ${activeTab === 'result' ? 'active' : ''}`}
            disabled={!recommendationResult}
            onClick={() => setActiveTab('result')}
          >
            <span className="step-num">2</span>
            <span>
              Kết quả Top-{searchForm.topK} & Điều chỉnh trực tiếp (CN02 + CN03)
            </span>
          </button>
        </div>

        <button
          type="button"
          className="theme-toggle-btn"
          onClick={toggleTheme}
          title={`Chuyển sang chế độ ${theme === 'dark' ? 'sáng' : 'tối'}`}
          aria-label={`Chế độ giao diện: ${theme === 'dark' ? 'Tối' : 'Sáng'}. Nhấn để đổi.`}
        >
          <span className="theme-toggle-icon" aria-hidden="true">
            {theme === 'dark' ? '☀️' : '🌙'}
          </span>
          <span>{theme === 'dark' ? 'Chế độ Sáng' : 'Chế độ Tối'}</span>
        </button>
      </nav>

      <AnimatePresence mode="wait">
        {activeTab === 'search' ? (
          <motion.div
            key="search-step"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
          >
            <SearchPage
              searchForm={searchForm}
              onChangeSearchForm={setSearchForm}
              onSubmitSearch={handleSubmitSearch}
              onApplyScenario={handleApplyScenario}
              isLoading={isLoading}
              apiError={apiError}
            />
          </motion.div>
        ) : (
          <motion.div
            key="result-step"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
          >
            <ResultPage
              recommendationResult={recommendationResult}
              searchContext={searchForm}
              onBackToSearch={() => setActiveTab('search')}
              onUpdatePriorities={handleUpdatePrioritiesLive}
              isUpdatingPriorities={isLoading && !!recommendationResult}
              isCalculating={isLoading && !recommendationResult}
              latencyMs={latencyMs}
              apiError={apiError}
              rankDeltas={rankDeltas}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  )
}

export default App

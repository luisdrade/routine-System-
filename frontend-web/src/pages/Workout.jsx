import { useState } from 'react'

export default function Workout() {
  const [setsCompleted, setSetsCompleted] = useState(0)

  const handleCompleteSet = () => {
    setSetsCompleted(prev => prev + 1)
  }

  return (
    <div className="page-content">
      <header>
        <h1 className="title">SUPINO RETO</h1>
        <p className="subtitle">Série {setsCompleted + 1} de 4</p>
      </header>

      <div className="info-row">
        <div className="info-box">
          <span className="info-label">CARGA</span>
          <span className="info-value">80 KG</span>
        </div>
        <div className="info-box">
          <span className="info-label">ALVO RPE</span>
          <span className="info-value">8.0</span>
        </div>
      </div>

      <div className="action-container">
        <button className="main-button" onClick={handleCompleteSet}>
          COMPLETAR SÉRIE
        </button>
      </div>
    </div>
  )
}
